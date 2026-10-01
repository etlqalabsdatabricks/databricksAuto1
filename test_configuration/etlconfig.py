# Databricks catalog and schema
CATALOG = "workspace"
SCHEMA = "default"

# Source tables (staging)
STAG_SUPPLIER = f"{CATALOG}.{SCHEMA}.stag_supplier"
STAG_PRODUCT = f"{CATALOG}.{SCHEMA}.stag_product"
STAG_STORES = f"{CATALOG}.{SCHEMA}.stag_stores"
STAG_SALES = f"{CATALOG}.{SCHEMA}.stag_sales"
STAG_INVENTORY = f"{CATALOG}.{SCHEMA}.stag_inventory"

# Target tables (fact/dimension)
FACT_SALES = f"{CATALOG}.{SCHEMA}.fact_sales"
FACT_INVENTORY = f"{CATALOG}.{SCHEMA}.fact_inventory"
MONTHLY_SALES_SUMMARY = f"{CATALOG}.{SCHEMA}.monthly_sales_summary"
INVENTORY_LEVEL_BY_STORES = f"{CATALOG}.{SCHEMA}.inventory_level_by_stores"

# Transformed tables
FILTERED_SALES = f"{CATALOG}.{SCHEMA}.filtered_sales"
HIGH_SALES = f"{CATALOG}.{SCHEMA}.high_sales"
LOW_SALES = f"{CATALOG}.{SCHEMA}.low_sales"

# Test data file paths (UC Volumes)
CSV_FILE_PATH = "/Volumes/workspace/default/etlqalabs_vol/netflix_dataset.csv"
JSON_FILE_PATH = "/Volumes/workspace/default/etlqalabs_vol/supplier_data.json"
XML_FILE_PATH = "/Volumes/workspace/default/etlqalabs_vol/inventory_data.xml"

# Reference table (currently available)
NETFLIX_TABLE = f"{CATALOG}.{SCHEMA}.netflix"

# Report and log paths
REPORT_DIR = "reports"
LOG_DIR = "logs"
DIFFERENCES_DIR = "differences"