print("Importing Data Service API")
import pandas as pd
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

# Instantiating a synchronous client with 120s timeout
client = httpx.Client(timeout=120.0)


# Generic function for making a request to the API given a formatted URL
def Make_Request(url: str):
    try:
        print(f"URL => {url}")
        response = client.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return []

#region Request Functions


def GetAllProvincialNOCHistoricData():
    try:
        url_to_call = f"{base_uri}{api_routes[4]}/"
        second_url_to_call = f"{base_uri}{api_routes[8]}/"
        province_history_data = Make_Request(url=url_to_call)
        province_data = Make_Request(url=second_url_to_call)

        province_df = pd.DataFrame(province_data)

        province_df = province_df[['provinceid', 'province_dguid']].rename(columns={'province_dguid':'dguid'})

        province_history_df = pd.DataFrame(province_history_data)
        data = province_history_df.merge(province_df, on='dguid')

        del province_history_df, province_df
        return data 
    except Exception as e:
        print(f"GetAllProvincialNOCHistoricData() => {e}")
        return pd.DataFrame()

