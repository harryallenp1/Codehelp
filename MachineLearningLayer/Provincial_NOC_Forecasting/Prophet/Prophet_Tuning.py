from MachineLearningLayer.Utils.Tuning import Tuner
from MachineLearningLayer.Utils.Splitter import Splitter
import pandas as pd
import warnings
import optuna
from prophet import Prophet
import os
from tqdm import tqdm
tqdm.pandas()
from sklearn.metrics import  mean_absolute_error
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_PATH = f"{BASE_DIR}/Prophet/Data/All_Hyperparams.json"


class TunerClass(Tuner):
    def __init__(self, data, meta_data):
        self.data = data
        self.meta_data = meta_data
        self.best_params = None

    def TuneModel(self):
        try:
            train = self.meta_data['Sets']['train'][['ds','y']]
            validate = self.meta_data['Sets']['validate'][['ds','y']]
            

            def objective(trial):
                params = {
                    "changepoint_prior_scale": trial.suggest_float("changepoint_prior_scale", 0.001, 0.5),
                    "changepoint_range": trial.suggest_float("changepoint_range", 0.5, 0.95),
                    "seasonality_prior_scale": trial.suggest_float("seasonality_prior_scale", 1.0, 20.0),
                    "holidays_prior_scale": trial.suggest_float("holidays_prior_scale", 1.0, 20.0),
                    "seasonality_mode": trial.suggest_categorical("seasonality_mode", ["additive", "multiplicative"]),
                    "weekly_seasonality": trial.suggest_int("weekly_seasonality", 3, 10),
                    "yearly_seasonality": trial.suggest_int("yearly_seasonality", 5, 20),
                    "growth": trial.suggest_categorical("growth", ["linear"]),
                }

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
                forecast = model.predict(validate)

                forecast = forecast.merge(validate, on='ds')

                mae = mean_absolute_error(forecast['y'], forecast['yhat'])

                return mae

            study = optuna.create_study(direction='minimize')
            study.optimize(objective, n_trials=50, timeout=120)

            best_params = study.best_params

            self.best_params = best_params

        except:
            pass
    
    def Save_Hyperparams(self):
        return self.best_params


def Load_Data(path=f'{BASE_DIR}/Prophet/Data/PreProcessed_Data.csv'):
    df = pd.read_csv(path)
    
    df['datestamp'] = pd.to_datetime(df['datestamp'])
    df = df.rename(columns={'datestamp':'ds','employment':'y'})

    keys = df['Key'].unique().tolist()

    return df, keys


def Generate_Sets(df):
    Set_Year_Markers = {
        'validateStart': 2024,
        'testStart': 2025
    }

    SplittObj = Splitter(Data=df, Set_Year_Markers=Set_Year_Markers)

    All_Sets = SplittObj.Generate_Sets()

    return All_Sets


def Tune_All(df, keys):
    try:
        
        All_Hyperparams = {}
        for key in tqdm(keys, desc='Processing Keys', unit='(provinceid, noc_groupingid)'):

            print(f"#Processing {key}#\n")

            data = df[df['Key']==key]

            
            data = data.sort_values(by='ds', ascending=True)

            All_Sets = Generate_Sets(df=data)

            meta_data = {
                'Key': key,
                'Sets': All_Sets
            }

            TuneObj = TunerClass(data=data, meta_data=meta_data)
            TuneObj.TuneModel()

            best_params = TuneObj.Save_Hyperparams()

            All_Hyperparams[key] = best_params
        
        
        with open(SAVE_PATH, "w") as file:
            json.dump(All_Hyperparams, file, indent=4)

        


    except Exception as e:
        print(f"Tune_All() => {e}")

if __name__ == '__main__':

    print(f"---Loading Data---\n")
    data, keys = Load_Data()

    print(f"---Running Tune---\n")

    Tune_All(df=data, keys=keys)