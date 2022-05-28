import { useState } from 'react';
import Header from '../../components/Header';
import DatePicker from 'react-datepicker';
import './home.css'

export default function Home(){

    const [startDateRegressao, setStartDateRegressao] = useState(new Date());
    const [endDateRegressao, setEndDateRegressao] = useState(new Date());
    const [startDatePrevisao, setStartDatePrevisao] = useState(new Date());
    const [endDatePrevisao, setEndDatePrevisao] = useState(new Date());

    function handleSubmit(e){
        e.preventDefault()
        alert('clicou')
    }

    return(
        <div>
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
            
        </div>
    )
}