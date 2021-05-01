# Celesc CDETL Pipeline

*Crawl, Download, Extract, Transform and Load Pipeline*

Repositorio que contém todo a aplicação responsável por:
- Logar no site da CELESC para determinado cliente usando um Crawler;
- Baixar todas as faturas em PDF da 2ªa via para este, usando o mesmo Crawler;
- Extrair e transformar os dados destes PDFs;
- Carregar estes em um CSV.

## Lógica abstrata do algoritmo ##
Os pipelines podem ser executados de forma separada:
- CD - Crawl and Download - Pipeline que loga no site da CELESC, e baixa todos os PDFs de 2ª via do cliente.
- ETL - Extract, Transform and Load - Pipeline que transforma os PDFs num único CSV contendo os dados.
>- Esse pipeline necessita de uma tabela no google sheets, de acordo com o modelo especificado no `database/g_sheets_config.md`

## Versão atual ##
Versão 1.0
Próxima versão -> Implementação da lógica de ETL para faturas do grupo A4.

## Principais arquivos do serviço ##
- `main_page.py`: Frontend da aplicação. É esse arquivo que você usará para interagir com a aplicação.
- `application/core_executor.py`: Quem gerencia todo o pipeline, podendo ser configurado para executar o pipeline de forma parcial ou completa;
- `application/variables_names.py`: Arquivo usado para configurar as variáveis do seu ambiente. Elas já estão configuradas, mas caso dê algum problema,
  tente primeiro ver se a causa é aqui.

## Como instalar na sua máquina via docker ##
1. Instale docker e docker-compose
2. Execute o docker, com base no arquivo `Makefile`

### 1. Docker Installation Tutorial ###
1. Install docker: https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt
2. Install docker-compose: https://docs.docker.com/compose/install/

### 2. Install the app requirements using Makefile ###
1. Install -> Run `make build`
2. Execute application -> Run `make up`
3. Stop application -> Run `make down`
4. Remove application (caso você queira apenas) -> `make down`

Opcionais:
- `make format`: Para formatar o código
- `make install`: Para apenas instalar o arquivo `requirements.txt`

## Running on cloud (AWS EC2) ##
https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3
