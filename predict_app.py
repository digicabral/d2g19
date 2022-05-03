from flask import Flask, request, jsonify
import pandas as pd
import joblib

app=Flask(__name__)

@app.route("/predict_one", methods=["GET"])
def predict():
    dados = pd.read_csv('data/predict_test.csv')
    model = joblib.load("models/model_pipeline.pkl")
    predictions = model.predict(dados)
    return predictions['yhat'].to_json(orient="records")

@app.route("/predict", methods=["GET"])
def predict_months():
    dados = request.get_json()
    return "Months"