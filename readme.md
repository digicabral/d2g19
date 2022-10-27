# Facebook Prophet D2G19

Algoritmo para previsão de turnover de colaboradores.

[![Build Status](https://github.com/facebook/prophet/workflows/Build/badge.svg)](https://facebook.github.io/prophet/)

## Pré-Requisitos
Ter o anaconda navigator instalado no sistema

Executar na ordem abaixo:

Salvar o dataset original com o nome dataset.xlsx na pasta "data" no mesmo formato que o primeiro enviado, mantendo a mesma nomenclatura, ordem, e tipos de dados das colunas\
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

<br/>

## Etapas do aprendizado
As colunas utilizadas para o aprendizado foram:

| dt_competencia | demitido  |  ativos  | admissoes | attrition | attrition_18a27 | attrition_27a30 | attrition_0a35 | attrition_35a40 | attrition_40mais |
| -------------- | ----------| -------- | --------- | --------- | --------------- | --------------- | -------------- | --------------- | ---------------- |
|                |           |          |           |           |                 |                 |                |                 |                  |

\
Sendo assim, removemos as demais colunas do dataset original, deixando apenas as listadas acima.
Além disso, o algoritmo Facebook Prophet exige que a coluna de data da série temporal seja renomeada para ds, e que a variável target seja renomeada para y para o aprendizado. Desta forma, criamos uma coluna de datas com o index do dataframe que era a data de competência (dt_competencia), e a renomeamos para ds, e a coluna attrition (variável target) foi renomeada para y.

\
Em seguida, rodamos uma função para encontrar os melhores hiperparâmetros, de acordo com a documentação do Facebook Prophet que pode ser acessada através do link: https://facebook.github.io/prophet/docs/diagnostics.html

\
Nesta função, criamos um dicionário python com algumas possibilidades de hiperparâmetros recomendados pela documentação, e criamos uma matriz com todas as combinações possíveis de parâmetros.

\
Em seguida, o algoritmo realiza um fit do modelo com todas estas possibilidades de parâmetros, e calcula o RMSE para cada um dos casos e os armazena em um dataframe com seus respectivos resultados.

\
Após isso, buscamos o menor rmse e seus respectivos hiperparâmetros dentro deste dataframe e aplicamos como retorno da função para ser utilizado no fit do modelo final.

\
No fit do modelo, o algoritmo utiliza as colunas listadas na tabela acima e realiza o aprendizado.

\
Por fim, com o modelo treinado, geramos o dump do modelo, através da função serialize_object() salvando no disco da máquina na pasta /models do projeto arquivo no formato .pkl, pronto para utilização para as previsões.

\
Em seguida rodamos a função run() que executa todos os processos listados acima na ordem definida.

<br/>

## Etapas para o forecast

Para realizar previsões, utilizamos o arquivo predict_app.py

Neste arquivo, realizamos a leitura do arquivo .pkl através da biblioteca joblib e da função criada read_model()

1 - Leitura dos dados de previsão informando neste arquivo as seguintes informações:

|      ds       |  demitido |  ativos  | admissoes | attrition_18a27 | attrition_27a30 | attrition_0a35 | attrition_35a40 | attrition_40mais |
| ------------- | ----------| -------- | --------- | --------------- | --------------- | -------------- | --------------- | ---------------- |
| datetime64[ns]|   float   |   float  |  float    |      float      |      float      |      float     |      float      |      float       |


2 - Chamamos o modelo através da função read_model()

3 - Armazenamos a previsão no dataframe "predictions"

Exemplo abaixo:

```python
dados = pd.read_csv('data/predict_test.csv')
model = read_model()
predictions = model.predict(dados)
```

No exemplo acima, realizamos a previsão para 1 mês. Entretanto, de acordo com o verificado com o cliente, na maioria dos casos serão realizadas previsões para vários meses, e como não possuímos os dados dos meses futuros em mãos para fornecer para o algoritmo e são eles que desejamos prever, criamos uma função que gera uma regressão linear baseada nos dados do dataset original para que possamos realizar previsões. Além disso, fornecemos para esta função os seguintes parâmetros:

\
1 - Data de Início para gerar a regressão baseada nos dados do dataset original.
\
Neste parâmetro, definimos a data de início da nossa regressão linear. Onde: os valores inputados não podem ser menores que a primeira data de competência da base (01/01/2018). Nem Maiores do que a última data de competência da base (01/12/2021). O valor deste campo deve sempre apontar para o primeiro dia do mês desejado. Valor exemplo: '01/07/2021'

\
2 - Data de Fim para gerar a regressão baseada nos dados do dataset original.
\
Neste parâmetro, definimos a data de fim da nossa regressão linear. Onde: os valores inputados não podem ser menores que a primeira data de competência da base (01/01/2018). Nem Maiores do que a última data de competência da base (01/12/2021). Nem menores do que a data de ínicio (parâmetro anterior). O valor deste campo deve sempre apontar para o primeiro dia do mês desejado. Valor exemplo: '01/12/2021'

\
3 - Data de início do dataset futuro (data de início do mês do intervalo que deseja prever).
\
Neste parâmetro definimos uma data de início superior à última data de competência registrada no dataset. O valor deste campo deve sempre apontar para o primeiro dia do mês desejado. Valor Exemplo: '01/01/2022'.

\
4 - Data de término do dataset futuro (data de início do último mês do intervalo que deseja prever).
\
Neste parâmetro definimos uma data superior à data de início do dataset futuro. O valor deste campo deve sempre apontar para o primeiro dia do mês desejado. Valor exemplo: '01/07/2022'

\
Com os parâmetros definidos conforme o exemplo acima, o algoritmo gera uma regressão dos dados necessários para a previsão baseada no período entre 07/2021 e 12/2021. E um dataset futuro com os meses entre 01/2022 e 07/2022 (meses que serão previstos o attrition). Desta forma, fica à critério do usuário a definição das datas desejadas para previsão e para input de dados.

<br/>

## Testando o ambiente
Após seguir o passo à passo dos pré requisitos, um teste pode ser realizado acessando através do navegador ou de alguma ferramenta de requisições HTTP (Postman, Insomnia, Thunder) a URL http://localhost:5000/predict_one.

\
O acesso à esta URL realiza uma requisição do tipo HTTP GET à API e retorna a previsão baseada nos dados de teste do arquivo predict_test.csv que se encontra na pasta /data do projeto.

<br/>

## Realizando previsões via API
Para realizar as previsões de vários meses, foi criada a rota /predict_months.

<br/>

Para utilizar esta rota é necessário realizar uma requisição HTTP do tipo POST, com o envio do tipo JSON no corpo da requisição na através da URL http://localhost:5000/predict_months.
Exemplo abaixo:

```json
{
    "data_ini_regressao": "01/05/2021",
    "data_fim_regressao": "01/12/2021",
    "dt_ini_previsao": "01/01/2022",
    "dt_fim_previsao": "01/07/2022"
}

```

<br/>

Onde: <br/>
data_ini_regressao  - define a data de início de utilização do dataset para gerar a regressão <br/>
data_fim_regressao  - define a data de fim de utilização do dataset para gerar a regressão <br/>
dt_ini_previsao - define a data de início das previsões <br/>
dt_fim_previsao - define a data de fim das previsões

<br/>

Se a requisição for realizada com sucesso, o código de status será o HTTP 200 e o retorno será um JSON contendo um array com as informações das previsões conforme o exemplo abaixo:
<br/>

```json
[
  {
    "ds": "01/01/2022",
    "yhat_lower": 59.684783704,
    "yhat_upper": 59.7624953741,
    "yhat": 59.7279478548
  }
]
```
<br/>
Onde:<br/>
ds - Data do mês previsto<br/>
yhat_lower - Valor mais baixo da previsão <br/>
yhat_upper - Valor mais alto da previsão <br/>
yhat - Valor da previsão
 <br/>
 <br/>

# Links das análises anteriores (colabs)
Todos os links abaixo nos levaram às conclusões descritas acima </br>
https://drive.google.com/file/d/12oDL_QFmLuLu6k1PaXOSo61QxSavNp7t/view?usp=sharing <br/>
https://colab.research.google.com/drive/13eGtQiXDXhZ-JPAFbxjRXM_PP5grEKJf?usp=sharing <br/>
https://colab.research.google.com/drive/1A_d6g8Sye-ZbKp-PVuz3CAFs17A9JpJS?usp=sharing <br/>
https://colab.research.google.com/drive/1ka3qi6y_8k-A_xTGsQUQGTxuHHdVJ2Lc?usp=sharing <br/>
https://colab.research.google.com/drive/1pAYurO2clN0FQ5TyP72O1xYg-4SmRZhc?usp=sharing <br/>
https://colab.research.google.com/drive/1TAWWL667PmvN09sh9xfkINopQhT579y5?usp=sharing <br/>
https://colab.research.google.com/drive/1rDwM_RKFtcx97TrtaXhqJePEULdoBhFQ?usp=sharing <br/>
https://colab.research.google.com/drive/1S3yOD1ibJpMPQz3L9IrKxfmO5Yt84m2J?usp=sharing
