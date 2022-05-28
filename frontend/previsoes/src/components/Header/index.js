import './header.css'
import Logo from '../../assets/logo_zup.png'

export default function Header(){
    return(
        <div className="header">
            <a href="#default" className="logo"><img src={Logo} alt="logo"/></a>
                <div className="header-right">
                    <h1>Previsão de Attrition</h1>
                </div>
        </div>
    )
}