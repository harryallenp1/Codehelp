#By: Ed Wang 
#Manipulating Data 

from DataTransportationLayer.DataServiceAPI import DataService
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
    'year':'Year'
}

KPI_Rename_Dict = {
    'employment_rate_2_years_after_graduating_field': 'Employment Rate 2 Years after Graduation',
    'employment_rate_6_months_after_graduating_field': 'Employment Rate 6 Months after Graduation',
    'graduation_rate': 'Graduation Rate',
    'university':'University',
    'programcategoryid':'ProgramID',
    'universityid':'UniversityID',
    'lat':'Lat',
    'lon':'Lon',
    'year':'Year'
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


def Get_All_Year_KPIs_For_Program(ProgramID, KPI):
    try:
        df = DataService.RequestKPIForProgram(ProgramID=ProgramID)

        df = df.rename(columns=KPI_Rename_Dict)

        df_Reduced = df[['Year','University', KPI]].sort_values(by=['Year','University'], ascending=[False,True])
        df_Reduced[KPI] = pd.to_numeric(df_Reduced[KPI], errors='coerce')
        df_Reduced[KPI] = round(df_Reduced[KPI] * 100, 2)
        Years = [2017,2018,2019,2020]
        df_Reduced = df_Reduced[df_Reduced['Year'].isin(Years)]
        df_pivot = df_Reduced.pivot(index='University', columns='Year', values=KPI)

        
       
        df_pivot['University'] = df_pivot.index
        df_pivot = df_pivot.reset_index(drop=True)
        
        
        df_pivot = df_pivot[['University'] + Years]

        print(df_pivot)
        print(df_pivot.columns)

        return df_pivot

    except Exception as e:
        print(f"Get_All_Year_KPIs_For_Program(ProgramID={ProgramID}) => {e}")
        return pd.DataFrame()
    


#region Forecasting Analysis Data Getters 

def Get_Provincial_NOC_Forecast(provinceid : int, noc_groupingid : int) -> pd.DataFrame:
    try:
        df = DataService.Request_Provincial_NOC_Forecast(provinceID=provinceid, noc_groupingid=noc_groupingid)

        df['yhat'] = df['yhat'].round(2)
        df['yhat_lower'] = df['yhat_lower'].round(2)
        df['yhat_upper'] = df['yhat_upper'].round(2)
        return df

    except Exception as e:
        print(f"Get_Provincial_NOC_Forecast(provinceid : {provinceid}, noc_groupingid : {noc_groupingid}) => {e}")
        return pd.DataFrame()


def Get_NOC_Forecast_All_Provinces(noc_groupingid : int) -> pd.DataFrame:
    try:
        df = DataService.Request_All_Province_NOC_Forecast(noc_groupingid=noc_groupingid)

        df = df.rename(columns={'province_shorthand':'Province','year':'Year'})

        df = df[df['Year']>=2026]

        # print(df)
        

        Years = sorted(df['Year'].unique())

        # print(f"Years =>\n{Years}")

        df = df.sort_values(by=['provinceid','Year'], ascending=[True,True])

        df_pivot = df.pivot(index='Province', columns='Year', values='Employment Forecast')

        df_pivot['Province'] = df_pivot.index
        df_pivot = df_pivot.reset_index(drop=True)

        df_pivot = df_pivot[['Province'] + Years]

        
        return df_pivot
    

    except Exception as e:
        print(f"Get_NOC_Forecast_All_Provinces(noc_groupingid : {noc_groupingid}) => {e}")
        return pd.DataFrame()
#endregion 
