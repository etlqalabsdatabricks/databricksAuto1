# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,Install pytest-html
# MAGIC %pip install pytest-html -q

# COMMAND ----------

# DBTITLE 1,Run All Tests
exec(open("/Workspace/Users/etlqalabsdatabricks@gmail.com/DataBricksAutomation/Runner.py").read())

# COMMAND ----------

