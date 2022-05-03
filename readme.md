# Facebook Prophet D2G19

Algoritmo para previsão de attrition.

## Pré-Requisitos
- Criar Ambiente virtual: conda create -n prophet python=3.8
- Ativar ambiente virtual: conda activate prophet
- conda install -c anaconda ephem
- conda install -c conda-forge pystan
- conda install -c conda-forge fbprophet
- conda install dask distributed -c conda-forge
- Instalar dependências na ordem listada: conda install --file requirements.txt
- Criar app Flask: set FLASK_APP=predict_app
- Rodar app Flask: flask run