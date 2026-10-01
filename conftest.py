import sys
import os
sys.dont_write_bytecode = True

import pytest
import logging
from pyspark.sql import SparkSession

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("differences", exist_ok=True)

logging.basicConfig(
    filename="logs/test_results.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Log test results automatically after each test."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        logger.info(f"{report.outcome.upper()} - {item.name}")


@pytest.fixture(scope="session")
def spark():
    """Provides a SparkSession for pytest tests."""
    logger.info("Creating SparkSession")
    spark_session = SparkSession.getActiveSession()
    if spark_session is None:
        from databricks.connect import DatabricksSession
        spark_session = DatabricksSession.builder.getOrCreate()
    logger.info("SparkSession created successfully")
    return spark_session