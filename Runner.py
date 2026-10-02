import sys, os
sys.dont_write_bytecode = True
os.chdir("/Workspace/Users/etlqalabsdatabricks@gmail.com/DataBricksAutomation")
import pytest
args = ["--junitxml=reports/test_results.xml"]
try:
    import pytest_html
    args += ["--html=reports/test_results.html", "--self-contained-html"]
except ImportError:
    pass
if globals().get("marker"):
    args[:0] = ["-m", marker]
pytest.main(args)