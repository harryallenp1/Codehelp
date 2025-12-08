"""
By Ed Wang

This module will run a unit-test simulation using the 'pytest' library. 
Each function starting with 'test_' runs a simulation of testing functions with certain parameters. 
The result of each test will be appended to a txt file denoted by RESULT_FILE.

JIRA Issue: PMP-84

"""

import pytest
from UnitTesting.ApplicationLayer.University_KPI_all_and_latest import *
import pandas as pd
from datetime import datetime

BASE = 'UnitTesting/ApplicationLayer/Results'
RESULT_FILE = f"{BASE}/university_kpi_all_and_latest.txt"

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
    (University_KPI_History_Check, (3,'Employment Rate 2 Years after Graduation')),
    (University_KPI_History_Check, (4,'Employment Rate 6 Months after Graduation')),
    (Latest_KPI_Program_data, (3,)),
    (Latest_KPI_Program_data, (4, ))

]

#Expected Success function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_SUCCESS_ENDPOINTS)
def test_expected_success(test_func, args):
    data = test_func(*args)

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

#endregion

#region -------- FAILURE TESTS -------- #
EXPECTED_FAILURE_ENDPOINTS = [
    (University_KPI_History_Check, (300,'employment_rate_6_years_after_graduating_field')),
    (University_KPI_History_Check, ('ABC','employment_rate_12_months_after_graduating_field')),
    (Latest_KPI_Program_data, (300,)),
    (Latest_KPI_Program_data, ('ABC', ))
]

#Expected Failure function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_FAILURE_ENDPOINTS)
def test_expected_failure(test_func, args):
    data = test_func(*args)

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
#endregion