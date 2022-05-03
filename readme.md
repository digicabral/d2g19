# Facebook Prophet D2G19

Algoritmo para previsão de attrition.

[![Build Status](https://github.com/facebook/prophet/workflows/Build/badge.svg)](https://facebook.github.io/prophet/)

## Pré-Requisitos
Executar na ordem abaixo:

Salvar o dataset original com o nome dataset.xlsx na pasta "data"
Criar Ambiente virtual:
```sh
conda create -n prophet python=3.8
```

Ativar ambiente virtual:
```sh
conda activate prophet
```

Instalar bibliotecas:

```sh
conda install -c anaconda ephem
conda install -c conda-forge pystan
conda install -c conda-forge fbprophet
conda install dask distributed -c conda-forge
```

Instalar dependências do requirements.txt
```sh
conda install --file requirements.txt
```
Criar app Flask
```sh
set FLASK_APP=predict_app
```

Rodar app Flask
```sh
flask run
```