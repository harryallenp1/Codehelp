from backend import DataUtils, GraphUtils


# df, Measure, Program = DataUtils.Get_Program_University_Data(ProgramID=1, Metric=1)

def Generate_Options(KeyDict):
    Options = [{'label':val, 'value':choice} for choice,val in KeyDict.items()]

    return Options

def Get_Program_Options():
    ProgramID_Programs_Dict = DataUtils.Get_Program_Options_Dict()

    return Generate_Options(KeyDict=ProgramID_Programs_Dict)

def Get_NOC_Options():
    NOC_NOC_Occupations_Dict = DataUtils.Get_NOC_Occupations_Dict()

    return Generate_Options(KeyDict=NOC_NOC_Occupations_Dict)

def Get_Post_Grad_Employment_Rate_Measure_Options():
    Program_Post_Grad_Employment_Rate_Dict = DataUtils.Get_Post_Grad_Employment_Measure_Dict()

    return Generate_Options(KeyDict=Program_Post_Grad_Employment_Rate_Dict)





# GraphUtils.Graph_Program_University_Post_Grad_Employment_Rate(Program=Program, Measure=Measure, Data=df)


def Generate_KPI_Comparison(Program, KPI):
    try:
        df, Measure, Program = DataUtils.Get_Program_University_Data(ProgramID=Program, Metric=KPI)
        Map = GraphUtils.Graph_Program_University_Post_Grad_Employment_Rate_Map(Program=Program, Measure=Measure, Data=df)
        Bar = GraphUtils.Graph_Program_University_Post_Grad_Employment_Rate_Bar(Program=Program, Measure=Measure, Data=df)

        return Map, Bar

    except Exception as e:
        print(f'Generate_KPI_Map(Program={Program}, KPI={KPI}) => {e}')
        return {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {Program}'}}, {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {Program} Bar'}}
    

def Generate_Program_Pathways(Program):
    try:
        df = DataUtils.Get_Program_Occupation_Data(ProgramID=Program)

        Mappings = GraphUtils.Generate_Program_to_Occupation_Mapping(Data=df)

        return Mappings
    
    except Exception as e:
        print(f"Generate_Program_Pathways(Program={Program}) => {e}")
        return {'data': [], 'layout': {'title': f'Program-Occupation Mappings Unavailable for {Program} Bar'}}
    

def Generate_NOC_History_In_Ontario(NOC_Code):
    try:
        df, NOC_Occupation = DataUtils.Get_NOC_Historical_Data(NOC_Code=NOC_Code)

        History_Graphs = GraphUtils.Generate_NOC_History(Data=df, NOC_Occupation=NOC_Occupation)

        return History_Graphs

    except Exception as e:
        print(f"Generate_NOC_History_In_Ontario(NOC_Code={NOC_Code}) => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History Unavailable'}}

def Generate_NOC_Latest_ER_PCT(NOC_Code):
    try:
        df, NOC_Occupation = DataUtils.Get_Latest_ER_NOC_PCT(NOC_Code=NOC_Code)

        ER_Bar = GraphUtils.Generate_NOC_ER_Stat(Data=df, NOC_Occupation=NOC_Occupation)

        return ER_Bar

    except Exception as e:
        print(f"Generate_NOC_Latest_ER_PCT(NOC_Code={NOC_Code}) => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History for ERs Unavailable'}}