# Como rodar o front-end

Como o front-end foi criado em react, é necessário um servidor rodando node.js para que a aplicação funcione corretamente. <br/>

Após a instalação do node, basta navegar até o reposítório, abrir no prompt de comando e digitar os seguintes comandos:

```
cd frontend
npm install
npm start
```
Isto irá rodar a aplicação em ambiente de desenvolvimento, e a mesma poderá ser acessada através da URL: <br/>
[http://localhost:3000](http://localhost:3000) no seu navegador.

## Para gerar o Build de produção:
### `npm run build`

Este comando gera a build de produção, e salva os arquivos na pasta `build`. <br/>

Com o build de produção em mãos, poderá ser rodado localmente ou em algum servidor de nuvem de sua preferência.