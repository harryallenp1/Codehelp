#By: Ed Wang 
#Manipulating Data 

from ApplicationLayer.DataServiceAPI import DataService
import pandas as pd 
import numpy as np


Latest_KPI_Rename_Dict = {
    'employment_rate_2_years_after_graduating_field': '2020 Employment Rate 2 Years after Graduation',
    'employment_rate_6_months_after_graduating_field': '2020 Employment Rate 6 Months after Graduation',
    'graduation_rate': '2020 Graduation Rate',
    'university':'University',
    'programcategoryid':'ProgramID',
    'universityid':'UniversityID',
    'lat':'Lat',
    'lon':'Lon',
}

Program_Links_Rename_Dict = {
    'programid' : 'ProgramID',
    'program' : 'Program',
    'broad_occupation_category':'Broad Occupation Category',
    'sub_major_group': 'Sub-Major Group',
    'unit_group_occupation': 'Unit Group Occupation'
}

Province_Employment_History_Dict = {
    'datestamp': 'ds',
    'employment':'Employment (Persons in Thousands)',
    'employment_moving_average':'3-Month Moving Average',
    'employment_upper_band':'Upper Band',
    'employment_lower_band': 'Lower Band'
}

Economic_Region_Employment_Dict = {
    'economicregion':'Economic Region',
    'employment_pct_change': 'Monthly PCT',
}

def Get_Program_University_Data(ProgramID):
    try:
        df = DataService.RequestLatestKPIForProgram(ProgramID=ProgramID)

        #We need to rename the columns so that there more readable. 
        df = df.rename(columns=Latest_KPI_Rename_Dict)

        return df

    except Exception as e:
        print(f"Get_Program_University_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame()

def Get_Program_Occupation_Data(ProgramID):
    try:
        df = DataService.RequestProgramNOCLinks(ProgramID=ProgramID)

        df = df.rename(columns=Program_Links_Rename_Dict)
        
        return df
    except Exception as e:
        print(f"Get_Program_Occupation_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame()

def Get_NOC_Historical_Data(NOC_GroupingID,DGUID='2021A000235'):
    try:
        df = DataService.RequestNOCGroupLaborStatistics(NOC_GroupingID=NOC_GroupingID,DGUID=DGUID)
        
        df = df.rename(columns=Province_Employment_History_Dict)

        return df

    except Exception as e:
        print(f"Get_NOC_Historical_Data(NOC_GroupingId={NOC_GroupingID},DGUID={DGUID}) => {e}")
        return pd.DataFrame()
    
def Get_Latest_ER_NOC_PCT(NOC_GroupingID, provinceID=35):
    try:
        df = DataService.RequestEconomicRegionEmploymentEstimate(NOC_GroupingID=NOC_GroupingID, ProvinceID=provinceID)
        
        df['employment_pct_change'] = pd.to_numeric(df['employment_pct_change'], errors='coerce')
        conditions = [
            df['employment_pct_change'] > 0,
            df['employment_pct_change'] < 0,
            df['employment_pct_change'] == 0
        ]
        choices = ['Increase', 'Decrease', 'No Change']
        df['Change'] = np.select(conditions, choices, default='No Data').astype(str)
        
        df = df.rename(columns=Economic_Region_Employment_Dict)



        return df

    except Exception as e:
        print(f"Get_Latest_ER_NOC_PCT(NOC_GroupingId={NOC_GroupingID},provinceID={provinceID}) => {e}")
        return pd.DataFrame()

