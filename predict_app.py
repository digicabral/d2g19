from flask import Flask, request, jsonify
import pandas as pd
import datetime as dt
import joblib

app=Flask(__name__)

def read_model():
    model = joblib.load("models/model_pipeline.pkl")
    return model

@app.route("/predict_one", methods=["GET"])
def predict():
    dados = pd.read_csv('data/predict_test.csv')
    model = read_model()
    predictions = model.predict(dados)
    return predictions['yhat'].to_json(orient="records")

@app.route("/predict", methods=["POST"])
def predict_months():
    dados = request.get_json()
    return "Months"