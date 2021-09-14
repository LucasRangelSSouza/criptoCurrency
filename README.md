![N|Solid](https://github.com/LucasRangelSSouza/criptoCurrency/blob/main/utils/capa.jpg)

# Programa: Cripto Currency
Este é um cliente desenvolvido em python e docker para obter dados dos preços de execução (cotações) de criptomoedas reportadas em tempo real, através de uma API pública,o sistema processa estas cotações e as 
agrega em candlesticks (com os dados de abertura, máxima, mínima e fechamento (saiba
mais [aqui ](https://pt.wikipedia.org/wiki/Candlestick) ) e salva estes candles em um banco de dados Mysql.
Foram implementados candles de 1min, 5min e 10min. 
A API  consumida é  a Poloniex Public API (mais especificamente o
comando returnTicker).

## Execução:
O programa é ser executado utilizando o docker compose, para tanto instale configure o docker em seu ambiente para testar a aplicação.
Apos instalado o docker em seu ambiente clone o repositorio.

###### 1º Clone o repositorio criptoCurrency
* Abra o o terminal de comandos do seu SO
* Navegue até um diretorio pre-existente de sua escolha:
    ```
    C:\> chdir C:\MeuDiretorio\
    ```
* Clone o repositorio criptoCurrency
    ```
    C:\> git clone https://github.com/LucasRangelSSouza/criptoCurrency
    ```
* Aguarde até que o download dos arquivos finalize

###### 2º Execute o docker compose
* Abra o o terminal de comandos do seu SO e Navegue até o diretorio onde o repositorio foi clonado:
    ```
    C:\> chdir C:\MeuDiretorio\criptoCurrency
    ```
* Realize o build:
    ```
    C:\> docker-compose build
    ```
* Inicie os containers:
    ```
    C:\> docker compose up -d
    ```
* Verifique se os containers foram iniciados com sucesso:
    ```
    C:\> docker ps -a
    ```
* Abaixo é possivel ver o passo a passo de forma ilustrada 
    
    ![](https://github.com/LucasRangelSSouza/criptoCurrency/blob/main/utils/docker.gif)

###### 3° Conectando ao banco de dados
* Para conectar ao banco de dados do container recomenda-se utilizar o mysql workbench, para como instalar e configurar o mysql workbench veja mais [aqui ](https://www.alura.com.br/artigos/mysql-do-download-e-instalacao-ate-sua-primeira-tabela?gclid=Cj0KCQjwkIGKBhCxARIsAINMioLm_sclhddLQPOnX3i7hsBt3H80xZ5-ENvxbmmUyq8ylPMDZhG7AfYaAtYnEALw_wcB.

* Por padrão as credenciais para acesso externo ao docker são:
 #
| Credencial | Valor | 
| ------ | ------ |
| host | localhost |
| porta | 3300 |
| user | admin |
| senha | 789123 |
| banco | currency |

* Por padrão as credenciais para acesso interno utilizando outro container docker são:
 #
| Credencial | Valor | 
| ------ | ------ |
| host | mysql |
| porta | 3306 |
| user | admin |
| senha | 789123 |
| banco | currency |
| docker network | default-network |

* Abaixo é possivel ver o passo a passo de forma ilustrada de como se conecta ao banco via mysql workbench, bem como uma analisé rapida da estrutura do banco.

    ![](https://github.com/LucasRangelSSouza/criptoCurrency/blob/main/utils/workbench.gif)
	
	
## Estrutura do banco de dados
* O banco de dados possui uma tabela TEMP, o qual tem dados de candles com uma periodicidade de 1 segundo dos ultimos 15 minutos de execução do programa, ele tambem possui a tabela CANDYSTICKS, no qual estão hospedados os dados dos cancles de 1 minuto, 5 minutos e 10 minutos de todas as 387 moedas oferecidas pela api da poloniex


## Estrutura da aplicação
A aplicação é estruturada em 5 containers:
* Container mysql - Este container hospeda o serviço do banco de dados MySql
* Container getDataApi - Este container obetem os candles com uma periodicidade de 1 segundo e salva na tablea TEMP do banco de dados.
* Container oneMinuteTicker - Este container formulas os candles de 1 minutos e os salva na tabela CANDYSTICKS
* Container fiveMinuteTicker - Este container formulas os candles de 5 minutos e os salva na tabela CANDYSTICKS
* Container tenMinuteTicker - Este container formulas os candles de 10 minutos e os salva na tabela CANDYSTICKS bem como remove os candles com idade superios a 15 minutos da tabela TEMP

----
### Licença
MIT
**Free Software, Hell Yeah!**

