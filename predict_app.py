from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import datetime as dt
import joblib
import json
from functools import reduce
from sklearn.linear_model import LinearRegression

app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def read_model():
    model = joblib.load("models/model_pipeline.pkl")
    return model

def load_data():
    df = pd.read_excel('data/dataset.xlsx', header=0, index_col=0, parse_dates=True, squeeze=True, engine='openpyxl')
    return df

def adjust_data(dataframe):
    #Removo as colunas que não serão utilizadas e deixo apenas as listadas abaixo e o index com a data
    df = dataframe.filter(['demitido','ativos','admissoes','attrition','attrition_18a27','attrition_27a30','attrition_0a35','attrition_35a40','attrition_40mais'])
    
    # Criando a coluna ds que é requisito obrigatório do prophet com as informações temporais e instanciando o modelo do prophet
    df = df.rename(columns={'attrition':'y'})
    df['ds'] = df.index.values
    
    # ordenando do mais antigo para o mais novo
    df = df.sort_index(axis=0)

    return df

def get_columns_regression():
  colunas = adjust_data(load_data()).columns.to_list()
  colunas.remove('y')
  colunas.remove('ds')
  return colunas

def generate_linear_regression(dt_ini_reg, dt_fim_reg, dt_ini_futuro, dt_fim_futuro):
  date_ini = dt.datetime.strptime(dt_ini_reg, "%d/%m/%Y").strftime('%Y-%m-%d')
  date_end = dt.datetime.strptime(dt_fim_reg, "%d/%m/%Y").strftime('%Y-%m-%d')

  datemin = dt.datetime.strptime(dt_ini_futuro, '%d/%m/%Y').date()
  datemax = dt.datetime.strptime(dt_fim_futuro, '%d/%m/%Y').date()

  #Carrego os dados
  df = adjust_data(load_data())
  #Filtro o dataset com o período que quero usar os dados para gerar a regressão
  mask = (df['ds'] >= date_ini) & (df['ds'] <= date_end)
  df_periodo_selecionado = df.loc[mask]
  #dropo a coluna y pois quem vai prever é o prophet
  df_periodo_selecionado.drop(columns='y',inplace=True)
  #Adiciono uma coluna de data ordinal
  df_periodo_selecionado['data_ordinal'] = df_periodo_selecionado['ds'].apply(lambda x: x.toordinal())

  colunas = get_columns_regression()
  dataframes = []

  for i, col in enumerate(colunas):
    x = df_periodo_selecionado[['data_ordinal']].to_numpy().reshape((-1,1))
    y = df_periodo_selecionado[[col]].to_numpy()
    reg = LinearRegression().fit(x, y)
    
    future = pd.DataFrame({'ds': pd.date_range(datemin, datemax, freq='MS')})
    future['ds'] = future['ds'].apply(lambda x: x.toordinal())
    future[col] = reg.predict(future)
    future['ds'] = future['ds'].astype(int).map(dt.datetime.fromordinal)

    dataframes.append(future)
  
  df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['ds'],
                                            how='inner'), dataframes)
  
  df_merged['y'] = np.NaN

  return df_merged

@app.route("/predict_one", methods=["GET"])
@cross_origin()
def predict():
    dados = pd.read_csv('data/predict_test.csv')
    model = read_model()
    predictions = model.predict(dados)
    return predictions['yhat'].to_json(orient="records")

@app.route("/predict_months", methods=["POST"])
@cross_origin()
def predict_months():
    #Recebe os dados do POST
    dadosRequest = request.get_json()
    
    #Pego as datas do POST e armazeno numa lista para serem utilizadas na geração dos dados futuros e da regressão linear
    date_list = []
    for data in dadosRequest.values():
        date_list.append(data)
    
    #Chamo a função que gera a regressão linear passando as datas do POST como parâmetro
    dadosFuturos = generate_linear_regression(date_list[0],date_list[1],date_list[2],date_list[3])

    #Instancio o modelo
    model = read_model()

    #Realizo as previsões usando os dados gerados na regressão linear e armazeno no dataframe
    predictions = model.predict(dadosFuturos)

    predictions.drop(predictions.columns.difference(['ds','yhat','yhat_lower','yhat_upper']),1,inplace=True)

    predictions['ds'] = predictions['ds'].dt.strftime('%d/%m/%Y')

    #Retorno as previsões como resposta do POST
    return predictions.to_json(orient="records")