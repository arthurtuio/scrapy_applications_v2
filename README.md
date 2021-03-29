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

## Versão atual ##
Versão XX.XX
Próxima versão -> Implementação da lógica de ETL para faturas do grupo A4.

## Principais arquivos do serviço ##
- `utils.py`: Arquivo usado para configurar as variáveis do seu ambiente -> No futuro vai virar um arquivo de docker pras variaveis de ambiente
- `core_executor.py`: Quem gerencia todo o pipeline, podendo ser configurado para executar o pipeline de forma parcial ou completa;
- `main_page.py`: Frontend da aplicação. É esse arquivo que você usará para interagir com a aplicação.

## Como instalar na sua máquina ##
1. Instale docker
2. Rode o docker e abraço
Brincadeira vou deixar completinho
