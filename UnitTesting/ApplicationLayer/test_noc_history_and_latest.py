'''
By Tejas Kumar

This module will run a unit-test simulation using the 'pytest' library. 
Each function starting with 'test_' runs a simulation of testing functions with certain parameters. 
The result of each test will be appended to a txt file denoted by RESULT_FILE.

JIRA Issue: PMP-85

'''



import pytest
from UnitTesting.ApplicationLayer.NOC_History_And_Latest import *
import plotly.graph_objs._figure
from datetime import datetime
import pandas as pd
import plotly.io as pio

BASE = 'UnitTesting/ApplicationLayer/Results'
RESULT_FILE = f"{BASE}/noc_history_and_latest_changes.txt"

#region Logger Function
def log_result(section: str, func_name: str, args: tuple, assert_desc: str, passed: bool, extra_info=""):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        status = "PASS" if passed else "FAIL"
        f.write(f"Expected [{section}] Function: {func_name}, Args: {args}, Assert: {assert_desc}, Result: {status}")
        if extra_info:
            f.write(f", Info: {extra_info}")
        f.write("\n")


with open(RESULT_FILE, "w", encoding="utf-8") as f:
    f.write(f"Test run started at {datetime.now()}\n\n")

#endregion

#region -------- SUCCESS TESTS -------- #
EXPECTED_SUCCESS_ENDPOINTS = [
    (Employment_History_Check, (26,)),
    (Employment_History_Check, (38,)),
    (Latest_Employment_Rates_For_ERs, (26,)),
    (Latest_Employment_Rates_For_ERs, (38, ))

]

#Expected Success function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_SUCCESS_ENDPOINTS)
def test_expected_success(test_func, args):
    data, graph = test_func(*args)

    try:
        assert len(data) != 0
        log_result("SUCCESS", test_func.__name__, args, "Data Is Not Empty", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "Data Is Empty", False)

    # Assert 2: Data is a pd.DataFrame
    try:
        assert isinstance(data, pd.DataFrame)
        log_result("SUCCESS", test_func.__name__, args, "The Data is a Pandas Dataframe", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "The Data is NOT a Pandas Dataframe", False, f"Got {type(data)}")

    # Assert 3: Graph is a plotly.dict and open the graph
    try:
        assert type(graph) == plotly.graph_objs._figure
        log_result("SUCCESS", test_func.__name__, args, "Plotly Figure", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "Not a Plotly Figure", False, f"Got {type(graph)}")

#endregion

#region -------- FAILURE TESTS -------- #
EXPECTED_FAILURE_ENDPOINTS = [
    (Employment_History_Check, (75,)),
    (Employment_History_Check, ('ASB',)),
    (Latest_Employment_Rates_For_ERs, (75,)),
    (Latest_Employment_Rates_For_ERs, ('ASB', ))
]

#Expected Failure function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_FAILURE_ENDPOINTS)
def test_expected_failure(test_func, args):
    data, graph = test_func(*args)

    # Assert 1: Data is Empty
    try:
        assert len(data) == 0
        log_result("FAIL", test_func.__name__, args, "Data Is Empty", True)
    except AssertionError:
        log_result("FAIL", test_func.__name__, args, "Data Is NOT Empty", False)

    # Assert 2: Data is a pd.DataFrame
    try:
        assert isinstance(data, pd.DataFrame)
        log_result("FAIL", test_func.__name__, args, "The Data is a Pandas Dataframe", True)
    except AssertionError:
        log_result("FAIL", test_func.__name__, args, "The Data is NOT a Pandas Dataframe", False, f"Got {type(data)}")

    # Assert 3: Graph is a plotly.dict and open the graph
    try:
        assert isinstance(graph, dict)
        log_result("FAIL", test_func.__name__, args, "Dict", True)
    except AssertionError:
        log_result("FAIL", test_func.__name__, args, "Not a Dict", False, f"Got {type(graph)}")

#endregion