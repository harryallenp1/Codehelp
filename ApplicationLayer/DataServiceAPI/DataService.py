#By: Tejas Kumar
#This module serves as helper to make API calls to the DataLayer endpoints
#It define functions and parameter to send to API and returns the relevant information in forms of dataframes. 
#This helps seperate out the data retrievel mechanism to a single module that can
print(f"Importing Data Service API")
import polars as pl
import pandas as pd
import httpx

base_uri = 'http://127.0.0.1:8000/api/'

api_routes = {
    1:'program_university_kpi_latest',
    2:'program_category',
    3: 'program_noc_link',
    4: 'provincial_noc_group_labor_statistic',
    5: 'noc_grouping',
    6: 'economic_region_employment_estimate',
    7: 'economicregion',
    8: 'province'
}

#Instantiating a Client that will attempt to make requests and will the connection if a response doesnt come back in atleast 30 seconds.
client = httpx.AsyncClient(timeout=30.0)

#Generic Function for making a request to the API given a formatted URL f-string 
async def Make_Request(url: str):
    try:
        print(f"URL => {url}")
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return []


#region Request Functions 

#Request Latest KPI Data for a given Program. 
async def RequestLatestKPIForProgram(ProgramID: int, Year=2020) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[1]}/?programcategoryid={ProgramID}&year={Year}"
        data = await Make_Request(url=url_to_call)
        df = pd.DataFrame(data)
        return df    
    except Exception as e:
        print(f'RequestLatestKPIForProgram(ProgramID={ProgramID}) => {e}')
        return pd.DataFrame()

#Request Yearly KPI Data for a Program at a University 
async def RequestKPIForProgramAndUniversity(ProgramID: int, UniversityID: int) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[1]}/?programcategoryid={ProgramID}&universityid={UniversityID}"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestKPIForProgramAndUniversity(ProgramID={ProgramID},UniversityID={UniversityID}) => {e}')
        return pd.DataFrame()

#Request Program Categories 
async def RequestProgramCategories() -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[2]}/"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestProgramCategories => {e}')
        return pd.DataFrame()

#Request NOC Grouping 
async def RequestNOCGroupingOptions() -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[5]}/"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestNOCGroupingOptions => {e}')
        return pd.DataFrame()

#Request Program NOC Link Data given a Program
async def RequestProgramNOCLinks(ProgramID: int) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[3]}/?programid={ProgramID}"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestProgramNOCLinks(ProgramID={ProgramID}) => {e}')
        return pd.DataFrame()

#Request NOC Group Labor Statistics given a Province DGUID and NOC_GroupingID 
async def RequestNOCGroupLaborStatistics(DGUID: str, NOC_GroupingID: int) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[4]}/?dguid={DGUID}&noc_groupingid={NOC_GroupingID}"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestNOCGroupLaborStatistics(DGUID={DGUID}, NOC_GroupingID={NOC_GroupingID}) => {e}')
        return pd.DataFrame()

#Request Economic Regions 
async def RequestEROptions(ProvinceID: int) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[7]}/?provinceid={ProvinceID}"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestEROptions(ProvinceID={ProvinceID}) => {e}')
        return pd.DataFrame()

#Request Economic Region Employment Estimates given a NOC_GroupingID and Province_ID
async def RequestEconomicRegionEmploymentEstimate(NOC_GroupingID: int, ProvinceID: int) -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[6]}/?noc_groupingid={NOC_GroupingID}"
        data = await Make_Request(url=url_to_call)
        df = pd.DataFrame(data).groupby('dguid').tail(1)

        df_ER_Names = await RequestEROptions(ProvinceID=ProvinceID)
        df_ER_Names = df_ER_Names.rename(columns={'economicregion_dguid':'dguid'})[['dguid','economicregion']]

        df_Merge = df_ER_Names.merge(df, on='dguid', how='right')
        return df_Merge
    except Exception as e:
        print(f'RequestEconomicRegionEmploymentEstimate(NOC_GroupingID={NOC_GroupingID}) => {e}')
        return pd.DataFrame()

#Requestion Proving Options 
async def RequestProvince() -> pd.DataFrame:
    try:
        url_to_call = f"{base_uri}{api_routes[8]}/"
        data = await Make_Request(url=url_to_call)
        return pd.DataFrame(data)
    except Exception as e:
        print(f'RequestProvince()  => {e}')
        return pd.DataFrame()


#endregion 


