import logging
import os
import pytest
from pyspark.sql import SparkSession
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/test_results.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class BaseUtility:
    """Base utility class with file reading and logging."""

    def _read_file(self, spark, file_path, file_type):
        if file_type == 'csv':
            return spark.read.option("header", "true").csv(file_path)
        elif file_type == 'json':
            return spark.read.json(file_path)
        elif file_type == 'xml':
            return spark.read.format("xml").option("rowTag", "item").load(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def read_file(self, spark, file_path, file_type):
        return self._read_file(spark, file_path, file_type)

    def log_info(self, message):
        logger.info(message)

    def log_error(self, message):
        logger.error(message)


class ValidationUtility(BaseUtility):
    """Validation utility for FILE_TO_DB and DB_TO_DB comparisons."""

    def execute_validation(self, validation_type, test_case_name, spark,
                           query_actual=None, table_actual=None,
                           file_path=None, file_type=None,
                           query_expected=None, table_expected=None):
        if validation_type == "FILE_TO_DB":
            self.validate_file_to_db(test_case_name, spark, file_path, file_type, query_actual)
        elif validation_type == 'DB_TO_DB':
            self.validate_db_to_db(test_case_name, spark, query_expected, query_actual)
        elif validation_type == 'TABLE_TO_TABLE':
            self.validate_table_to_table(test_case_name, spark, table_expected, table_actual)

    def validate_file_to_db(self, test_case_name, spark, file_path, file_type, query_actual):
        try:
            df_expected = self.read_file(spark, file_path, file_type)
            df_actual = spark.sql(query_actual)
            self._compare_dataframes(test_case_name, df_expected, df_actual)
        except Exception as e:
            logger.error(f"{test_case_name} validation failed: {e}")
            pytest.fail(f"{test_case_name} validation failed: {e}")

    def validate_db_to_db(self, test_case_name, spark, query_expected, query_actual):
        try:
            df_expected = spark.sql(query_expected)
            df_actual = spark.sql(query_actual)
            self._compare_dataframes(test_case_name, df_expected, df_actual)
        except Exception as e:
            logger.error(f"{test_case_name} validation failed: {e}")
            pytest.fail(f"{test_case_name} validation failed: {e}")

    def validate_table_to_table(self, test_case_name, spark, table_expected, table_actual):
        try:
            df_expected = spark.table(table_expected)
            df_actual = spark.table(table_actual)
            self._compare_dataframes(test_case_name, df_expected, df_actual)
        except Exception as e:
            logger.error(f"{test_case_name} validation failed: {e}")
            pytest.fail(f"{test_case_name} validation failed: {e}")

    def _compare_dataframes(self, test_case_name, df_expected, df_actual):
        expected_count = df_expected.count()
        actual_count = df_actual.count()
        logger.info(f"{test_case_name} - expected rows: {expected_count}, actual rows: {actual_count}")
        assert expected_count == actual_count, (
            f"{test_case_name} failed: row count mismatch - expected={expected_count}, actual={actual_count}"
        )
        logger.info(f"{test_case_name} passed")


class DataQualityUtility(BaseUtility):
    """Data quality checks for duplicates and nulls."""

    def check_duplicate_in_file(self, spark, file_path, file_type):
        try:
            df = self.read_file(spark, file_path, file_type)
            total = df.count()
            distinct = df.distinct().count()
            return total == distinct
        except Exception as e:
            logger.error(f"Duplicate check failed: {e}")

    def check_duplicate_in_table(self, spark, table_name):
        try:
            df = spark.table(table_name)
            total = df.count()
            distinct = df.distinct().count()
            return total == distinct
        except Exception as e:
            logger.error(f"Duplicate check failed: {e}")

    def check_duplicate_for_column(self, spark, file_path, file_type, column_name):
        try:
            df = self.read_file(spark, file_path, file_type)
            total = df.count()
            distinct = df.select(column_name).distinct().count()
            return total == distinct
        except Exception as e:
            logger.error(f"Column duplicate check failed: {e}")

    def check_null_values_in_file(self, spark, file_path, file_type):
        try:
            df = self.read_file(spark, file_path, file_type)
            null_count = df.filter(" OR ".join(f"{c} IS NULL" for c in df.columns)).count()
            return null_count == 0
        except Exception as e:
            logger.error(f"Null check failed: {e}")

    def check_null_values_for_column(self, spark, file_path, file_type, column_name):
        try:
            df = self.read_file(spark, file_path, file_type)
            null_count = df.filter(f"{column_name} IS NULL").count()
            return null_count == 0
        except Exception as e:
            logger.error(f"Column null check failed: {e}")


class FileUtility(BaseUtility):
    """File existence and size checks."""

    def check_file_existence(self, file_path):
        try:
            return os.path.exists(file_path)
        except Exception as e:
            logger.error(f"File existence check failed: {e}")
            return False

    def check_file_size(self, file_path):
        try:
            return os.path.getsize(file_path) > 0
        except Exception as e:
            logger.error(f"File size check failed: {e}")
            return False


class SchemaValidationUtility(BaseUtility):
    """Schema validation for column names, datatypes, and referential integrity."""

    def validate_column_names(self, spark, table_name, expected_columns):
        df = spark.table(table_name)
        actual_columns = df.columns
        assert actual_columns == expected_columns, (
            f"Column mismatch in table {table_name}: "
            f"expected={expected_columns}, actual={actual_columns}"
        )

    def validate_column_datatypes(self, spark, table_name, expected_datatypes):
        df = spark.table(table_name)
        for column_name, expected_type in expected_datatypes.items():
            actual_type = dict(df.dtypes)[column_name]
            assert actual_type == expected_type, (
                f"Datatype mismatch in table {table_name}: "
                f"column={column_name}, expected={expected_type}, actual={actual_type}"
            )

    def check_referential_integrity(self, spark, source_table, target_table, key_column):
        try:
            source_df = spark.table(source_table)
            target_df = spark.table(target_table)
            source_keys = source_df.select(key_column).distinct()
            target_keys = target_df.select(key_column).distinct()
            orphans = source_keys.exceptAll(target_keys)
            orphan_count = orphans.count()
            assert orphan_count == 0, (
                f"Referential integrity failed: {orphan_count} orphaned records in {source_table}"
            )
        except Exception as e:
            logger.error(f"Referential integrity check failed: {e}")
            pytest.fail(f"Referential integrity check failed: {e}")