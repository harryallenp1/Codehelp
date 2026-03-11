'''
By: Tejas Kumar 

This module represents the calling of endpoints to test the DJANGO Api provided by the data layer. 
Each Function makes a call to an end point. 

So Far only Get Endpoint are being tested.
'''

import httpx

base_uri = 'http://127.0.0.1:8000/api/'

api_routes = {
    1: 'program_university_kpi_latest',
    2: 'program_category',
    3: 'program_noc_link',
    4: 'provincial_noc_group_labor_statistic',
    5: 'noc_grouping',
    6: 'economic_region_employment_estimate',
    7: 'economicregion',
    8: 'province',
    9: 'university'
}

client = httpx.Client(timeout=120.0)


def Make_Request(url: str) -> dict:
    try:
        
        response = client.get(url)
        
        ReponseInfo = {
           'status': response.status_code,
           'data': response.json()
        }
         
        return ReponseInfo
    except Exception as e:
        print(f"Request failed for {url}: Error => [{e}]")
        return {
            'status': 'Not Specified',
            'data': {},
        }

#region GET 

#region Filtered Endpoint Calls 
def Test_KPI_Endpoint(ProgramID: int) -> tuple:
    
    url = f"{base_uri}{api_routes[1]}/?programcategoryid={ProgramID}"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']


def Test_Program_NOC_Link_Endpoint(ProgramID: int) -> tuple:
    
    url = f"{base_uri}{api_routes[3]}/?programid={ProgramID}"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

def Test_Provincial_NOC_Labor_Stats_Endpoint(DGUID: str, NOC_GroupingID: int) -> tuple:
    
    url = f"{base_uri}{api_routes[4]}/?dguid={DGUID}&noc_groupingid={NOC_GroupingID}"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

def Test_ER_NOC_Labor_Stats_Endpoint(NOC_GroupingID: int, ProvinceID: int) -> tuple:
        
    url = f"{base_uri}{api_routes[6]}/?noc_groupingid={NOC_GroupingID}/provinceid={ProvinceID}"
    ResponseInfo = Make_Request(url=url)    
    return ResponseInfo['status'], ResponseInfo['data']

#endregion


#region Entities Endpoints
def Test_Program_Categories_Endpoint() -> tuple:
    url = f"{base_uri}{api_routes[2]}/"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

def Test_Univeristy_Endpoint() -> tuple:
    url = f"{base_uri}{api_routes[9]}/"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

def Test_Province_Endpoint() -> tuple:
    url = f"{base_uri}{api_routes[8]}/"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

def Test_EconomicRegion_Endpoint() -> tuple:
    url = f"{base_uri}{api_routes[7]}/"
    ResponseInfo = Make_Request(url=url)
    return ResponseInfo['status'], ResponseInfo['data']

#endregion 
#endregion 