#By: Tejas Kumar 

from ApplicationLayer.DataServiceAPI import DataService

def Get_Program_Options():
    
    df = DataService.RequestProgramCategories()
    df = df.loc[df['programcategoryid'].isin([3,4])]
    ProgramOptions = df.set_index('programcategoryid')['programcategory'].to_dict()
    return ProgramOptions 


def Get_NOC_GroupOptions():
    df = DataService.RequestNOCGroupingOptions()
    NOC_Grouping_Options = df.set_index('noc_groupingid')['noc_grouping'].to_dict()
    return NOC_Grouping_Options


def Get_Province_Options():
    df = DataService.RequestProvince()
    ProvinceOptions = df.set_index('provinceid')['province'].to_dict()
    return ProvinceOptions


