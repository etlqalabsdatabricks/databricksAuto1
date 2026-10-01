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
class TestDataTransformation:
    validation_utility = ValidationUtility()

    @pytest.mark.smoke
    def test_data_transformation_filter_sales(self, spark):
        """Validate filtered_sales transformation."""
        test_case_name = "test_data_transformation_filter_sales"
        expected_query = f"SELECT * FROM {STAG_SALES} WHERE sale_date >= '2024-09-01'"
        actual_query = f"SELECT * FROM {FILTERED_SALES}"
        self.validation_utility.execute_validation(
            validation_type="DB_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            query_expected=expected_query,
            query_actual=actual_query,
        )

    @pytest.mark.regression
    def test_data_transformation_router_high_sales(self, spark):
        """Validate high_sales routing transformation."""
        test_case_name = "test_data_transformation_router_high_sales"
        expected_query = f"SELECT * FROM {FILTERED_SALES} WHERE region='High'"
        actual_query = f"SELECT * FROM {HIGH_SALES}"
        self.validation_utility.execute_validation(
            validation_type="DB_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            query_expected=expected_query,
            query_actual=actual_query,
        )

    def test_data_transformation_router_low_sales(self, spark):
        """Validate low_sales routing transformation."""
        test_case_name = "test_data_transformation_router_low_sales"
        expected_query = f"SELECT * FROM {FILTERED_SALES} WHERE region='Low'"
        actual_query = f"SELECT * FROM {LOW_SALES}"
        self.validation_utility.execute_validation(
            validation_type="DB_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            query_expected=expected_query,
            query_actual=actual_query,
        )

    # Assignment: Add aggregator and joiner transformation tests
    def test_data_transformation_aggregator_sales(self, spark):
        pass

    def test_data_transformation_joiner(self, spark):
        pass