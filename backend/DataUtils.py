'''
This file allows for data manipulation and retrieval for the backend services.
It uses Polars for efficient data handling and Pandas for compatibility with other libraries.
'''

print(f"Importing DataUtils\n")

import polars as pl
import pandas as pd 
import os 
import numpy as np

#Storing data paths.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAM_UNIVERSITY_DATA_PATH = os.path.join(BASE_DIR, "Data", "Tbl_ProgramUniversity.csv")
PROGRAMS_DATA_PATH = os.path.join(BASE_DIR, "Data", "Tbl_Programs.csv")
PROGRAM_OCCUPATIONS_PATH = os.path.join(BASE_DIR, "Data", "Tbl_ProgramOccupations.csv")
NOC_OCCUPATION_TS_PATH = os.path.join(BASE_DIR, "Data", "Tbl_SampleTimeSeries.csv")
NOC_OCCUPATION_ER_TS_PATH = os.path.join(BASE_DIR, "Data", "Tbl_SampleERTimeSeries.csv")

#Creating Lazy Polars DataFrames for efficient querying.
dp_Tbl_Program_University = pl.scan_csv(PROGRAM_UNIVERSITY_DATA_PATH)
dp_Tbl_Program_Occupations = pl.scan_csv(PROGRAM_OCCUPATIONS_PATH)
dp_Tbl_NOC_Occupation_TS = pl.scan_csv(NOC_OCCUPATION_TS_PATH)
dp_Tbl_NOC_ER_Occupations_TS = pl.scan_csv(NOC_OCCUPATION_ER_TS_PATH)

df_Tbl_Programs = pd.read_csv(PROGRAMS_DATA_PATH)


NOC_NOC_Name_Dict = dp_Tbl_NOC_Occupation_TS.select(['NOC Code','NOC Occupation']).unique().collect().to_pandas().set_index('NOC Code')['NOC Occupation'].to_dict()
ProgamID_Program_Dict = df_Tbl_Programs.set_index('ProgramID')['Program'].to_dict()


Program_Post_Grad_Employment_Rate_Dict = {
    1: '2020 Employment Rate 6 Months after Graduation',
    2: '2020 Employment Rate 2 Years after Graduation'
}

#region Deticated Functions for data retrieval.

def Get_NOC_Occupations_Dict():
    return NOC_NOC_Name_Dict


def Get_Program_Options_Dict():
    return ProgamID_Program_Dict

def Get_Post_Grad_Employment_Measure_Dict():
    return Program_Post_Grad_Employment_Rate_Dict



def Get_Program_University_Data(ProgramID, Metric):
    try:
        MetricName = Program_Post_Grad_Employment_Rate_Dict[Metric]
        Program = ProgamID_Program_Dict[ProgramID]
        df = dp_Tbl_Program_University.filter(pl.col('ProgramID')==ProgramID).select(['ProgramID','Program','UniversityID','University',MetricName,'Lat','Lon']).collect().to_pandas()

        return df, MetricName, Program
    

    except Exception as e:
        print(f"Get_Program_University_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame(), '', ''


def Get_Program_Occupation_Data(ProgramID):
    try:
        

        df = dp_Tbl_Program_Occupations.filter(pl.col('ProgramID').is_in(ProgramID)).collect().to_pandas()

        return df

    except Exception as e:
        print(f"Get_Program_Occupation_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame()
    

def Get_NOC_Historical_Data(NOC_Code):
    try:
        NOC_Occupation = NOC_NOC_Name_Dict[NOC_Code]

        df = dp_Tbl_NOC_Occupation_TS.filter(pl.col('NOC Code')==NOC_Code).collect().to_pandas().sort_values(by='ds', ascending=True)

        return df, NOC_Occupation
    

    except Exception as e:
        print(f"Get_NOC_Historical_Data(NOC_Code={NOC_Code}) => {e}")
        return pd.DataFrame(), ""


def Get_Latest_ER_NOC_PCT(NOC_Code):
    try:
        NOC_Occupation = NOC_NOC_Name_Dict[NOC_Code]

        df = dp_Tbl_NOC_ER_Occupations_TS.filter(pl.col('NOC Code')==NOC_Code).collect().to_pandas().sort_values(by='ds', ascending=True)

        df = df.groupby(['Economic Region']).tail(1)

        df['Monthly PCT'] = pd.to_numeric(df['Monthly PCT'], errors='coerce')

        conditions = [
            df['Monthly PCT'] > 0,
            df['Monthly PCT'] < 0,
            df['Monthly PCT'] == 0
        ]

        choices = ['Lift', 'Drop', 'No Change']

        df['Change'] = np.select(conditions, choices, default='No Change').astype(str)

        return df, NOC_Occupation

    except Exception as e:
        print(f"Get_Latest_ER_NOC_PCT(NOC_Code={NOC_Code}) => {e}")
        return pd.DataFrame(), ''
#endregion