from isort import file
import joblib
import pandas as pd
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from math import sqrt
import datetime as dt
import matplotlib.pyplot as plt
import itertools
from functools import reduce


# Load Data
def load_data():
    df = pd.read_excel('data/dataset.xlsx', header=0, index_col=0, parse_dates=True, squeeze=True, engine='openpyxl')
    return df

# Adjusting data
def adjust_data(dataframe):
    #Removo as colunas que nao serão utilizadas e deixo apenas as listadas abaixo e o index com a data
    df = dataframe.filter(['demitido','ativos','admissoes','attrition','attrition_18a27','attrition_27a30','attrition_0a35','attrition_35a40','attrition_40mais'])
    
    # Criando a coluna ds que é requisito obrigatório do prophet com as informações temporais e instanciando o modelo do prophet
    df = df.rename(columns={'attrition':'y'})
    df['ds'] = df.index.values
    
    # ordenando do mais antigo para o mais novo
    df = df.sort_index(axis=0)

    #Separamos os datasets em 80% para treino e 20% para teste caso necessário,
    #Mas nesta função todo o dataset está sendo utilizado para realizar o predict real com os dados de 2022 que ainda não existem
    split_point = int((len(df)/100)*80)
    df_train = df[0:split_point]
    df_test = df[split_point:]

    # write to disk
    df_train.to_csv('data/df_train.csv')
    df_test.to_csv('data/df_test.csv')

    return df

#Função para encontrar os melhores hiperparâmetros de acordo com a documentação do Facebook Prophet
#https://facebook.github.io/prophet/docs/diagnostics.html
def best_params(dataframe):
    # connect to the cluster
    client = Client()
    param_grid = {  
            'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
            'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
            }
    # Generate all combinations of parameters
    all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
    rmses = []  # Armazena todos os RMSEs para cada parâmetro
    # Usando cross validation para avaliar todos os parâmetros
    for params in all_params:
        # Fit model with given params
        m = Prophet(**params).fit(dataframe)
        df_cv = cross_validation(m, horizon='180 days', initial='180 days', period='180 days', parallel="dask")
        df_p = performance_metrics(df_cv, rolling_window=1)
        rmses.append(df_p['rmse'].values[0])
    #Find the best parameters
    tuning_results = pd.DataFrame(all_params)
    tuning_results['rmse'] = rmses
    best_params = all_params[np.argmin(rmses)]
    return best_params

#Função de Treino
def train(dataframe, params):
  model = Prophet(**params)
  #Faço um for adicionando todas as colunas exceto a attrition e o y que é a target, e o ds que é a data
  for col in dataframe.columns:
    if col not in["attrition","ds","y"]:
      model.add_regressor(col)
  model = model.fit(dataframe)
  return model


#Função para gerar o arquivo pickle
def serialize(model):
    joblib.dump(model, filename="models/model_pipeline.pkl")

    
#Função que roda o pipeline
def run():
    df = adjust_data(load_data())
    best_param = best_params(df)
    model = train(df, best_param)
    serialize(model)

if __name__ == "__main__":
    run()