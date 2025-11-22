from MachineLearningLayer.Utils.Forecast import Forecaster
from MachineLearningLayer.Utils.Splitter import Splitter
import pandas as pd
import warnings
from prophet import Prophet
import os
from tqdm import tqdm
tqdm.pandas()
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HypereparamsPath = f'{BASE_DIR}/Prophet/Data/All_Hyperparams.json'

SAVE_PATH = f"{BASE_DIR}/Prophet/Data/All_Forecasts.parquet"


class Prophet_Forecaster(Forecaster):
    def __init__(self, data, meta_data):
        self.data = data
        self.meta_data = meta_data
        self.forecast_data = None


    def Generate_Forecasts(self):
        try:
            print(f"Training Model")
            train = self.meta_data['Sets']['train'][['ds','y']]
            validate = self.meta_data['Sets']['validate'][['ds','y']]
            test = self.meta_data['Sets']['test'][['ds','y']]

            validateFull = self.meta_data['Sets']['validate']
            testFull = self.meta_data['Sets']['test']

            params = self.meta_data['Hyperparams']

            model = Prophet(
                    changepoint_prior_scale=params["changepoint_prior_scale"],
                    changepoint_range=params["changepoint_range"],
                    seasonality_prior_scale=params["seasonality_prior_scale"],
                    holidays_prior_scale=params["holidays_prior_scale"],
                    seasonality_mode=params["seasonality_mode"],
                    weekly_seasonality=params["weekly_seasonality"],
                    yearly_seasonality=params["yearly_seasonality"],
                    growth=params["growth"],
                )
            
            model.fit(train)
            valforecast = model.predict(validate)
            testforecast = model.predict(test)

            valforecast = valforecast.merge(validateFull, on='ds')
            testforecast = testforecast.merge(testFull, on='ds')

            future = model.make_future_dataframe(
                periods=48,
                freq='M'
            )

            futureforecast = model.predict(future)
            futureforecast['Key'] = self.meta_data['Key']

            Info = validateFull[['Key','provinceid','dguid','noc_groupingid']]

            futureforecast['year'] = futureforecast['ds'].dt.year

            futureforecast = futureforecast.merge(Info, on='Key')

            futureforecast = futureforecast.drop_duplicates(subset='ds')


            forecast_data = pd.concat([valforecast, testforecast, futureforecast], axis=0)

            self.forecast_data = forecast_data


        except Exception as e:
            print(f"{e}")
            pass

    def Save_Forecasts(self):
        return self.forecast_data


def Load_Data(path=f'{BASE_DIR}/Prophet/Data/PreProcessed_Data.csv'):
    df = pd.read_csv(path)
    
    df['datestamp'] = pd.to_datetime(df['datestamp'])
    df = df.rename(columns={'datestamp':'ds','employment':'y'})

    keys = df['Key'].unique().tolist()

    return df, keys

def Load_Hyperparams(path=HypereparamsPath):
    with open(path, 'r') as f:
        Hyperparams = json.load(f)
    
    return Hyperparams

def Generate_Sets(df):
    Set_Year_Markers = {
        'validateStart': 2024,
        'testStart': 2025
    }

    SplittObj = Splitter(Data=df, Set_Year_Markers=Set_Year_Markers)

    All_Sets = SplittObj.Generate_Sets()

    return All_Sets

def Generate_All_Forecasts(df , Hyperparams):
    try:

        keys = list(Hyperparams.keys())
        All_Forecasts = []
        for key in tqdm(keys, desc='Processing Keys', unit='(provinceid, noc_groupingid)'):
            print(f"#Processing {key}#\n")

            data = df[df['Key']==key]
            data = data.sort_values(by='ds', ascending=True)


            All_Sets = Generate_Sets(df=data)

            params = Hyperparams[key]


            meta_data = {
                'Key': key,
                'Sets': All_Sets,
                'Hyperparams': params
            }

            ForecastObj = Prophet_Forecaster(data=data, meta_data=meta_data)
            
            ForecastObj.Generate_Forecasts()

            forecast_data = ForecastObj.Save_Forecasts()

            All_Forecasts.append(forecast_data)

        df_All_Forecasts = pd.concat(All_Forecasts, axis=0)
        df_All_Forecasts.to_parquet(SAVE_PATH, index=False)

        print(df_All_Forecasts[['Key','ds','y','yhat']])

        print(f"---Forecasts Saved---")



    except Exception as e:
        print(f"Exceptions => [{e}]")
        pass


if __name__ == '__main__':

    print(f"---Loading Hyperparams---\n")
    Hyperparams = Load_Hyperparams()

    print(f"---Loading Data---\n")
    df, _ = Load_Data()

    print(f"---Generating Forecasts---\n")
    Generate_All_Forecasts(df=df, Hyperparams=Hyperparams)