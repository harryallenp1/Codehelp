'''
By: Ed Wang

This module represents the use case of getting all the University KPI statistics and
the latest University KPI statistics

JIRA Issue: PMP-84
'''

from ApplicationLayer.LogicalOperations import DataUtils


BASE = 'UnitTesting/ApplicationLayer/Results'

def University_KPI_History_Check(ProgramID,KPI):
    
    df = DataUtils.Get_All_Year_KPIs_For_Program(ProgramID=ProgramID,KPI=KPI)

    return df


def Latest_KPI_Program_data(ProgramID):
        df = DataUtils.Get_Program_University_Data(ProgramID=ProgramID)

        return df