#By: Ed Wang 
#Manipulating Data 

# from ApplicationLayer.LogicalOperations import OptionsUtils
from ApplicationLayer.DataServiceAPI import DataService
import pandas as pd 
import asyncio



async def Get_Program_University_Data(ProgramID):
    try:
        df = await DataService.RequestLatestKPIForProgram(ProgramID=ProgramID)
        return df
    

    except Exception as e:
        print(f"Get_Program_University_Data(ProgramID={ProgramID})=>{e}")
        return pd.DataFrame()


#Testing -> Open CMD and navigate to Education-Planning-Dashboard, then run python -m ApplicationLayer.LogicalOperations.DataUtils

df= asyncio.run(Get_Program_University_Data(ProgramID=3))


print(df)