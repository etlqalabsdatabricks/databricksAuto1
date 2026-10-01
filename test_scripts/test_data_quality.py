import pytest
import logging
from common_utilities.utilities import DataQualityUtility, FileUtility
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/test_results.log",
    filemode='a',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("spark")
class TestDataQuality:
    data_quality_utility = DataQualityUtility()
    file_utility = FileUtility()

    @pytest.mark.regression
    def test_data_quality_duplicate_check_csv(self, spark):
        """Check for duplicates in CSV file."""
        test_case_name = "test_data_quality_duplicate_check_csv"
        logger.info(f"Test case: {test_case_name} started")
        duplicate_status = self.data_quality_utility.check_duplicate_in_file(
            spark, CSV_FILE_PATH, "csv"
        )
        assert duplicate_status is True, "Duplicates found in CSV file"
        logger.info(f"Test case: {test_case_name} completed")

    @pytest.mark.regression
    @pytest.mark.DataQuality
    def test_data_quality_null_check_csv(self, spark):
        """Check for null values in CSV file."""
        test_case_name = "test_data_quality_null_check_csv"
        logger.info(f"Test case: {test_case_name} started")
        null_status = self.data_quality_utility.check_null_values_in_file(
            spark, CSV_FILE_PATH, "csv"
        )
        assert null_status is True, "Null values found in CSV file"
        logger.info(f"Test case: {test_case_name} completed")

    @pytest.mark.regression
    def test_data_quality_file_existence_csv(self, spark):
        """Check if CSV file exists."""
        test_case_name = "test_data_quality_file_existence_csv"
        logger.info(f"Test case: {test_case_name} started")
        file_status = self.file_utility.check_file_existence(CSV_FILE_PATH)
        assert file_status is True, "CSV file does not exist"
        logger.info(f"Test case: {test_case_name} completed")

    @pytest.mark.regression
    @pytest.mark.DataQuality
    @pytest.mark.smoke
    def test_data_quality_file_size_csv(self, spark):
        """Check if CSV file is not empty."""
        test_case_name = "test_data_quality_file_size_csv"
        logger.info(f"Test case: {test_case_name} started")
        file_size_status = self.file_utility.check_file_size(CSV_FILE_PATH)
        assert file_size_status is True, "CSV file is empty"
        logger.info(f"Test case: {test_case_name} completed")

    @pytest.mark.regression
    def test_data_quality_duplicate_check_table(self, spark):
        """Check for duplicates in Databricks table."""
        test_case_name = "test_data_quality_duplicate_check_table"
        logger.info(f"Test case: {test_case_name} started")
        duplicate_status = self.data_quality_utility.check_duplicate_in_table(
            spark, NETFLIX_TABLE
        )
        assert duplicate_status is True, "Duplicates found in table"
        logger.info(f"Test case: {test_case_name} completed")

    # Assignment: Add DQ tests for JSON, XML files
    def test_data_quality_duplicate_check_json(self, spark):
        pass

    def test_data_quality_null_check_json(self, spark):
        pass