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
class TestDataLoading:
    validation_utility = ValidationUtility()

    def test_data_loading_monthly_sales_summary(self, spark):
        """Validate monthly_sales_summary table loading."""
        test_case_name = "test_data_loading_monthly_sales_summary"
        expected_query = f"SELECT product_id, year, month, total_sales FROM {MONTHLY_SALES_SUMMARY}_source ORDER BY product_id"
        actual_query = f"SELECT product_id, year, month, total_sales FROM {MONTHLY_SALES_SUMMARY} ORDER BY product_id"
        self.validation_utility.execute_validation(
            validation_type="DB_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            query_expected=expected_query,
            query_actual=actual_query,
        )

    def test_data_loading_fact_inventory(self, spark):
        """Validate fact_inventory table loading."""
        test_case_name = "test_data_loading_fact_inventory"
        expected_query = f"SELECT product_id, store_id, quantity_on_hand, last_updated FROM {STAG_INVENTORY} ORDER BY product_id, store_id"
        actual_query = f"SELECT product_id, store_id, quantity_on_hand, last_updated FROM {FACT_INVENTORY} ORDER BY product_id, store_id"
        self.validation_utility.execute_validation(
            validation_type="DB_TO_DB",
            test_case_name=test_case_name,
            spark=spark,
            query_expected=expected_query,
            query_actual=actual_query,
        )

    # Assignment: Add loading tests for remaining target tables
    def test_data_loading_fact_sales(self, spark):
        pass

    def test_data_loading_inventory_level_by_stores(self, spark):
        pass