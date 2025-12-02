'''
By Tejas Kumar

This module will run a unit-test simulation using the 'pytest' library. 
Each function starting with 'test_' runs a simulation of testing functions with certain parameters. 
The result of each test will be appended to a txt file denoted by RESULT_FILE.

'''

import pytest
from Endpoints import *
from datetime import datetime

RESULT_FILE = "endpoint_test_results.txt"

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
    (Test_KPI_Endpoint, (3,)),
    (Test_Program_NOC_Link_Endpoint, (4,)),
    (Test_Provincial_NOC_Labor_Stats_Endpoint, ("2021A000235", 4)),
    (Test_ER_NOC_Labor_Stats_Endpoint, (3, '2021A000235')),
    (Test_Program_Categories_Endpoint, ()),
    (Test_Univeristy_Endpoint, ()),
    (Test_Province_Endpoint, ()),
    (Test_EconomicRegion_Endpoint, ()),
]

#Expected Success function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_SUCCESS_ENDPOINTS)
def test_expected_success(test_func, args):
    status, data = test_func(*args)

    # Assert 1: Status == 200
    try:
        assert status == 200
        log_result("SUCCESS", test_func.__name__, args, "status == 200", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "status == 200", False, f"Got {status}")

    # Assert 2: Data is not empty
    try:
        assert data
        log_result("SUCCESS", test_func.__name__, args, "data not empty", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "data not empty", False, f"Got {data}")

    # Assert 3: Data type
    try:
        assert isinstance(data, (dict, list))
        log_result("SUCCESS", test_func.__name__, args, "data type dict/list", True)
    except AssertionError:
        log_result("SUCCESS", test_func.__name__, args, "data type dict/list", False, f"Got {type(data)}")

#endregion

#region -------- FAILURE TESTS -------- #
EXPECTED_FAILURE_ENDPOINTS = [
    (Test_KPI_Endpoint, ("three",)),
    (Test_Program_NOC_Link_Endpoint, ("Tiger",)),
    (Test_Provincial_NOC_Labor_Stats_Endpoint, (64, "ABC")),
    (Test_ER_NOC_Labor_Stats_Endpoint, ({}, 'bikes')),
]

#Expected Failure function that checks multiple conditions and appends the results to the log.
@pytest.mark.parametrize("test_func, args", EXPECTED_FAILURE_ENDPOINTS)
def test_expected_failure(test_func, args):
    status, data = test_func(*args)

    # Assert 1: Status != 200
    try:
        assert status != 200
        log_result("FAILURE", test_func.__name__, args, "status != 200", True)
    except AssertionError:
        log_result("FAILURE", test_func.__name__, args, "status != 200", False, f"Got {status}")

    # Assert 2: Status in (400,404,500)
    try:
        assert status in (400, 404, 500)
        log_result("FAILURE", test_func.__name__, args, "status in (400,404,500)", True)
    except AssertionError:
        log_result("FAILURE", test_func.__name__, args, "status in (400,404,500)", False, f"Got {status}")

    # Assert 3: Data is empty
    try:
        assert not data
        log_result("FAILURE", test_func.__name__, args, "data empty", True)
    except AssertionError:
        log_result("FAILURE", test_func.__name__, args, "data empty", False, f"Got {data}")

#endregion