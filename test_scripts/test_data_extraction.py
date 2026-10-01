import pytest
import logging
from common_utilities.utilities import ValidationUtility
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/test_results.log",
    filemode='a',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("spark")
class TestDataExtraction:
    validation_utility = ValidationUtility()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_data_extraction_from_csv_to_table(self, spark):
        """Validate CSV file row count matches Databricks table."""
        test_case_name = "test_data_extraction_from_csv_to_table"
        actual_query = f"SELECT * FROM {NETFLIX_TABLE}"
        self.validation_utility.execute_validation(
            validation_type="FILE_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            file_path=CSV_FILE_PATH,
            file_type="csv",
            query_actual=actual_query,
        )

    # Assignment: Add extraction tests for JSON, XML files to staging tables
    def test_data_extraction_from_json_to_stage(self, spark):
        pass

    def test_data_extraction_from_xml_to_stage(self, spark):
        pass