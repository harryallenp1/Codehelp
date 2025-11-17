#By: Tejas Kumar
#Integrating Application Layer Utilities for usage. 

from ApplicationLayer.LogicalOperations import DataUtils, GraphUtils, OptionsUtils
import pandas as pd

print(f"Importing Dash App Utilities 2")

#An abstract function for Generating a key pair list for dropdown options in Dash.
def Generate_Options(KeyDict):
    Options = [{'label':val, 'value':choice} for choice,val in KeyDict.items()]

    return Options

#region Instantiating Main Selection Options 
def Get_All_Options_Dicts() -> tuple:
    try:
    
        ProgramDict = OptionsUtils.Get_Program_Options()
        NocOptionsDict = OptionsUtils.Get_NOC_GroupOptions()


        return ProgramDict, NocOptionsDict
    
    except Exception as e:
        print(f'Get_All_Options_Dicts() => {e}')
        return ()
    

ProgramDict, NocOptionsDict = Get_All_Options_Dicts()

print(ProgramDict)

Program_Post_Grad_Employment_Rate_Dict = {
    1: '2020 Employment Rate 6 Months after Graduation',
    2: '2020 Employment Rate 2 Years after Graduation',
    3: '2020 Graduation Rate',
}
#endregion
#  
#region Functions for Generating Dropdown Options.
def Get_Program_Options():

    return Generate_Options(KeyDict=ProgramDict)

def Get_NOC_Options():

    return Generate_Options(KeyDict=NocOptionsDict)

def Get_Post_Grad_Employment_Rate_Measure_Options():

    return Generate_Options(KeyDict=Program_Post_Grad_Employment_Rate_Dict)


#endregion

#region Functions for Program Search Page
def Generate_KPI_Comparison(ProgramID, KPI):
    try:
        
        #Data Utils Responsibility 
        df = DataUtils.Get_Program_University_Data(ProgramID=ProgramID)

        Program = ProgramDict[ProgramID]
        Measure = Program_Post_Grad_Employment_Rate_Dict[KPI]
        df['Program'] = df['ProgramID'].map(ProgramDict)
        df = df.dropna(subset=[Measure])
        df[Measure] = df[Measure].astype(float)

        #Graph Utils Responsibility 

        Map = GraphUtils.Graph_Program_University_Post_Grad_Employment_Rate_Map(Program=Program, Measure=Measure, Data=df)
        Bar = GraphUtils.Graph_Program_University_Post_Grad_Employment_Rate_Bar(Program=Program, Measure=Measure, Data=df)

        return Map, Bar


    except Exception as e:
         print(f'Generate_KPI_Map(Program={ProgramID}, KPI={KPI}) => {e}')
         return {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {ProgramDict[ProgramID]}'}}, {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {ProgramID[ProgramDict]} Bar'}}

#endregion 

#region Functions for Career Pathway Page 
def Generate_Program_Pathways(Program):
    try:
        df = DataUtils.Get_Program_Occupation_Data(ProgramID=Program)

        Mappings = GraphUtils.Generate_Program_to_Occupation_Mapping(Data=df)

        return Mappings
    
    except Exception as e:
        print(f"Generate_Program_Pathways(Program={Program}) => {e}")
        return {'data': [], 'layout': {'title': f'Program-Occupation Mappings Unavailable for {Program} Bar'}}



def Generate_NOC_History_In_Ontario(NOC_GroupingID):

    try:
        NOC_Occupation = NocOptionsDict[NOC_GroupingID]
        df = DataUtils.Get_NOC_Historical_Data(NOC_GroupingID=NOC_GroupingID)

        History_Graphs = GraphUtils.Generate_NOC_History(Data=df, NOC_Occupation=NOC_Occupation)

        return History_Graphs

    except Exception as e:
        print(f"Generate_NOC_History_In_Ontario(NOC_Code={NOC_GroupingID}) => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History Unavailable'}}

def Generate_NOC_Latest_ER_PCT(NOC_GroupingID):
    try:
        df = DataUtils.Get_Latest_ER_NOC_PCT(NOC_GroupingID=NOC_GroupingID)

        NOC_Occupation = NocOptionsDict[NOC_GroupingID]

        ER_Bar = GraphUtils.Generate_NOC_ER_Stat(Data=df, NOC_Occupation=NOC_Occupation)

        return ER_Bar

    except Exception as e:
        print(f"Generate_NOC_Latest_ER_PCT(NOC_Code={NOC_GroupingID}) => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History for ERs Unavailable'}}

#endregion
