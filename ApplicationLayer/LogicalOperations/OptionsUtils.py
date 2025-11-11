#By: Tejas Kumar 

from ApplicationLayer.DataServiceAPI import DataService

async def Get_Program_Options():
    
    df = await DataService.RequestProgramCategories()
    ProgramOptions = df.set_index('programcategoryid')['programcategory'].to_dict()
    return ProgramOptions 


async def Get_NOC_GroupOptions():
    df = await DataService.RequestNOCGroupingOptions()
    NOC_Grouping_Options = df.set_index('noc_groupingid')['noc_grouping'].to_dict()
    return NOC_Grouping_Options


async def Get_Province_Options():
    df = await DataService.RequestProvince()
    ProvinceOptions = df.set_index('provinceid')['province'].to_dict()
    return ProvinceOptions


