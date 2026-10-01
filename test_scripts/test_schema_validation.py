import pytest
import logging
from common_utilities.utilities import SchemaValidationUtility
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/test_results.log",
    filemode='a',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("spark")
class TestSchemaValidation:
    schema_validation = SchemaValidationUtility()

    @pytest.mark.smoke
    def test_table_column_names(self, spark):
        """Validate column names of the table."""
        expected_columns = [
            "show_id", "type", "title", "director", "cast",
            "country", "date_added", "release_year", "rating",
            "duration", "listed_in", "description",
        ]
        self.schema_validation.validate_column_names(
            spark, NETFLIX_TABLE, expected_columns
        )
        logger.info("Column names validation passed")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_table_column_datatypes(self, spark):
        """Validate column datatypes of the table."""
        expected_datatypes = {
            "show_id": "string",
            "type": "string",
            "title": "string",
            "director": "string",
            "cast": "string",
            "country": "string",
            "date_added": "string",
            "release_year": "bigint",
            "rating": "string",
            "duration": "string",
            "listed_in": "string",
            "description": "string",
        }
        self.schema_validation.validate_column_datatypes(
            spark, NETFLIX_TABLE, expected_datatypes
        )
        logger.info("Column datatypes validation passed")

    def test_referential_integrity_fact_sales_product_id(self, spark):
        """Check referential integrity for product_id between fact_sales and stag_product."""
        self.schema_validation.check_referential_integrity(
            spark, FACT_SALES, STAG_PRODUCT, "product_id"
        )
        logger.info("Referential integrity check passed")

    # Assignment: Add schema validation for remaining tables
    def test_fact_inventory_column_names(self, spark):
        pass

    def test_monthly_sales_summary_column_names(self, spark):
        pass

    def test_inventory_level_by_stores_column_names(self, spark):
        pass