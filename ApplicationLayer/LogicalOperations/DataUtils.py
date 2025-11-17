#By: Ed Wang 
#Manipulating Data 

from ApplicationLayer.DataServiceAPI import DataService
import pandas as pd 


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
        
        return df
    except Exception as e:
        print(f"Get_Program_Occupation_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame()

def Get_NOC_Historical_Data(NOC_GroupingID,DGUID):
    try:
        df = DataService.RequestNOCGroupLaborStatistics(NOC_GroupingID=NOC_GroupingID,DGUID=DGUID)

        return df

    except Exception as e:
        print(f"Get_NOC_Historical_Data(NOC_GroupingId={NOC_GroupingID},DGUID={DGUID}) => {e}")
        return pd.DataFrame()
    
def Get_Latest_ER_NOC_PCT(NOC_GroupingID, provinceID):
    try:
        df = DataService.RequestEconomicRegionEmploymentEstimate(NOC_GroupingID=NOC_GroupingID, provinceID=provinceID)

        return df

    except Exception as e:
        print(f"Get_Latest_ER_NOC_PCT(NOC_GroupingId={NOC_GroupingID},provinceID={provinceID}) => {e}")
        return pd.DataFrame()

