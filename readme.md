# Facebook Prophet D2G19

Algoritmo para previsão de attrition.

[![Build Status](https://github.com/facebook/prophet/workflows/Build/badge.svg)](https://facebook.github.io/prophet/)

## Pré-Requisitos
Ter o anaconda navigator instalado no sistema

Executar na ordem abaixo:

Salvar o dataset original com o nome dataset.xlsx na pasta "data" no mesmo formato que o primeiro enviado, com a mesma nomenclatura, ordem de colunas e tipos de dados\
\
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

## Etapas do aprendizado
As colunas utilizadas para o aprendizado foram:

| dt_competencia | demitido  |  ativos  | admissoes | attrition | attrition_18a27 | attrition_27a30 | attrition_0a35 | attrition_35a40 | attrition_40mais |
| -------------- | ----------| -------- | --------- | --------- | --------------- | --------------- | -------------- | --------------- | ---------------- |
|                |           |          |           |           |                 |                 |                |                 |                  |

\
Sendo assim, removemos as demais colunas do dataset original, deixando apenas as listadas acima.
Além disso, o algoritmo Facebook Prophet exige que a coluna de data da série temporal seja renomeada para ds, e que a variável target seja renomeada para y para o aprendizado. Sendo assim, criamos uma coluna de datas com o index do dataframe que era a data de competência, e a renomeamos para ds, e a coluna attrition (variável target) foi renomeada para y.

\
Em seguida, rodamos uma função para encontrar os melhores hiperparâmetros, de acordo com a documentação do Facebook Prophet que pode ser acessada através do link: https://facebook.github.io/prophet/docs/diagnostics.html

\
Nesta função, criamos um dicionário python com os hiperparâmetros recomendados pela documentação, e criamos uma matriz com todas as combinações possíveis de parâmetros.

\
Em seguida, o algoritmo realiza um fit do modelo com todas estas possibilidades de parâmetros, e calcula o rmse e os armazena em um dataframe para cada um dos casos.

\
Após isso, buscamos o menor rmse e seus respectivos hiperparâmetros dentro deste dataframe e aplicamos como retorno da função para ser utilizado no fit do modelo final.


## Etapas para o forecast
Para realizar uma previsão, é necessário fornecer para o algoritmo as seguintes colunas:

|      ds       |  demitido |  ativos  | admissoes | attrition_18a27 | attrition_27a30 | attrition_0a35 | attrition_35a40 | attrition_40mais |
| ------------- | ----------| -------- | --------- | --------------- | --------------- | -------------- | --------------- | ---------------- |
| datetime64[ns]|   float   |   float  |  float    |      float      |      float      |      float     |      float      |      float       |

## Utilização dos arquivos .pkl