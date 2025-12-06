'''
By: Tejas Kumar 

This module represents the use case of getting the historical employment trend for an NOC AND 
the latest PCT change in employment per Economic Region. 

JIRA Issue: PMP-85
'''


from ApplicationLayer.LogicalOperations import DataUtils, GraphUtils
import plotly.io as pio

BASE = 'UnitTesting/ApplicationLayer/Results'
def Employment_History_Check(NOC_GroupingID):
    
    df = DataUtils.Get_NOC_Historical_Data(NOC_GroupingID=NOC_GroupingID)

    History_Graphs = GraphUtils.Generate_NOC_History(Data=df, NOC_Occupation=None)

    pio.write_html(History_Graphs,f'{BASE}/{NOC_GroupingID}_Graph_Sample_History.html',auto_open=True)


    return df, History_Graphs


def Latest_Employment_Rates_For_ERs(NOC_GroupingID):
        df = DataUtils.Get_Latest_ER_NOC_PCT(NOC_GroupingID=NOC_GroupingID)


        ER_Bar = GraphUtils.Generate_NOC_ER_Stat(Data=df, NOC_Occupation=None)

        pio.write_html(ER_Bar,f'{BASE}/{NOC_GroupingID}_Graph_Sample_Latest_For_ER.html',auto_open=True)

        return df,ER_Bar