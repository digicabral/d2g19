import { useState } from 'react';
import Header from '../../components/Header';
import DatePicker from 'react-datepicker';
import './home.css'
import axios from 'axios';
import Plot from 'react-plotly.js'

export default function Home(){

    const [startDateRegressao, setStartDateRegressao] = useState(new Date());
    const [endDateRegressao, setEndDateRegressao] = useState(new Date());
    const [startDatePrevisao, setStartDatePrevisao] = useState(new Date());
    const [endDatePrevisao, setEndDatePrevisao] = useState(new Date());
    const [previsoes, setPrevisoes] = useState([])

    function formataData(data){
        var dataParam = data,
            dia  = '01',
            diaF = (dia.length === 1) ? '0'+dia : dia,
            mes  = (dataParam.getMonth()+1).toString(), //+1 pois no getMonth Janeiro começa com zero.
            mesF = (mes.length === 1) ? '0'+mes : mes,
            anoF = dataParam.getFullYear();
        return diaF+"/"+mesF+"/"+anoF;
    }

    function handleSubmit(e){
        e.preventDefault()
        getPredictions(formataData(startDateRegressao), 
                       formataData(endDateRegressao),
                       formataData(startDatePrevisao),
                       formataData(endDatePrevisao)
                        )
    }

    async function getPredictions(dtIniReg, dtFimReg, dtIniPrev, dtFimPrev){
        let data = {
            "data_ini_regressao": dtIniReg,
            "data_fim_regressao": dtFimReg,
            "dt_ini_previsao": dtIniPrev,
            "dt_fim_previsao": dtFimPrev
        }
        axios.post('http://localhost:5000/predict_months', data)
        .then((response)=>{
            setPrevisoes(response.data)
            console.log(previsoes)
        })
        .catch((error)=>{
            console.log(error)
        })
    }

   function transformDataChart(dados){
        let plot_data = []
        let x = []
        let y = []
        dados.map(each => {
            x.push(each.ds)
            y.push(each.yhat)
        })
        plot_data['x'] = x;
        plot_data['y'] = y

        console.log(plot_data)
        
        return plot_data
    }
    
    return(
        <div className="outside-div">
            <Header/>
            <div className='container-center'>
                <div className='date-selection'>
                    <form onSubmit={handleSubmit}>
                        <label>Mês de Início da Regressão</label>
                        <DatePicker
                            selected={startDateRegressao}
                            onChange={(date) => setStartDateRegressao(date)}
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                            showFullMonthYearPicker
                        />
                        <label>Mês de Fim da Regressão</label>
                        <DatePicker
                            selected={endDateRegressao}
                            onChange={(date) => setEndDateRegressao(date)}
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                            showFullMonthYearPicker
                        />
                        <label>Mês de Início da Previsão</label>
                        <DatePicker
                            selected={startDatePrevisao}
                            onChange={(date) => setStartDatePrevisao(date)}
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                            showFullMonthYearPicker
                        />
                        <label>Mês de Término da Previsão</label>
                        <DatePicker
                            selected={endDatePrevisao}
                            onChange={(date) => setEndDatePrevisao(date)}
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                            showFullMonthYearPicker
                        />
                        <button type="submit" >Gerar Previsões</button>
                    </form>
                </div>
            </div>
            <div className="container-return">
            {previsoes.length === 0 ? (
                <div></div>
            ) : (
                
                <div>
                    <div className='grafico'>
                    <Plot
                        data={[
                            {
                                x: transformDataChart(previsoes)['x'],
                                y: transformDataChart(previsoes)['y'],
                                type: 'scatter'
                            }
                        ]}
                        layout={
                            { width: 1300, 
                              height:600, 
                              title: 'Previsão de Attrition',
                              yaxis: {
                                  rangemode: 'tozero',
                                  autorange: true
                              }
                             }
                        }
                    />
                    </div>
                <br></br>
        
                <table>
                <thead>
                    <tr>
                        <th scope="col">Mês Ref.</th>
                        <th scope="col">Y</th>
                        <th scope="col">Y Upper</th>
                        <th scope="col">Y Lower</th>
                    </tr>
                </thead>
                <tbody>
                    {previsoes.map((item, index)=>{
                        return(
                            <tr key={index}>
                                <td data-label="Mês Ref.">{item.ds}</td>
                                <td data-label="Y">{item.yhat}</td>
                                <td data-label="Y Upper">{item.yhat_upper}</td>
                                <td data-label="Y Lower">{item.yhat_lower}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
            </div>
            )
            }
            </div>           
        </div>
    )
}