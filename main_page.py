import streamlit as st

from core_executor import CoreExecutor
from frontend.streamlit_dash import StreamlitDash
from utils.rename_scrapy_output import count_number_of_pdfs, generate_csv_to_download


class MainPage:
    def execute(self):
        st.markdown("""
            # GIDE Main Web Page #

            Página criada para gerenciar os pipelines de coleta e extração de
            dados de faturas da CELESC.

            Selecione no canto esquerdo a operação que você deseja realizar:

        _____________
        """)

        lista_operacoes = [
            "0. Página inicial",
            "1. Baixar PDFs do site da CELESC",
            "2. Criar CSVs das faturas",
            "3. Dashboard do CSV"
        ]

        operacao_selecionada = st.sidebar.selectbox("Operação escolhida", lista_operacoes)

        if operacao_selecionada == lista_operacoes[1]:
            self._download_celesc_faturas_as_pdfs()

        elif operacao_selecionada == lista_operacoes[2]:
            self._convert_faturas_to_csv()

        elif operacao_selecionada == lista_operacoes[3]:
            StreamlitDash().execute()

    @staticmethod
    def _download_celesc_faturas_as_pdfs():
        st.markdown("""
            ## Crawl and Download Pipeline ##
            
            Pipeline que loga no site da CELESC, e baixa todos os PDFs de 2ª via do cliente.
            
            Aperte o botão abaixo para que seja feito o download das faturas do primeiro
            cliente que se encontra na planilha referência.
            
            **Observação: A cada clique é executado todo este pipeline, então
            só aperte ele caso realmente necessário. **
        """)
        if st.button("Fazer download das faturas"):
            CoreExecutor(enable_download_from_site=True).execute()

        if st.checkbox("Conferir quantidade de PDFs baixados?"):
            st.markdown(f"""
            - Quantidade: {count_number_of_pdfs()["count"]}
            - Pasta em que se encontram: `{count_number_of_pdfs()["folder"]}`
            """)

    @staticmethod
    def _convert_faturas_to_csv():
        st.markdown("""
            ## ETL Pipeline ##
            
            Pipeline que transforma os PDFs num único CSV contendo os dados.
            
            Aperte o botão abaixo para que seja feita a conversão e seja
            criado o CSV.
            
            **Observação: A cada clique é executado todo este pipeline, então
            só aperte ele caso realmente necessário. **
            
            Caso você queira baixar o CSV em seu computador, selecione a opção presente
            na checkbox.
            
            Caso você queira conferir um dashboard criado a partir deste CSV, acesse
            a opção no canto esquerdo
            
            ```3. Visualizar resultados das faturas adicionadas no CSV```
            
        """)
        if st.button("Converter faturas de PDF para CSV"):
            CoreExecutor(enable_transform_in_csv=True).execute()

        if st.checkbox("Baixar CSV no seu PC?"):
            download_link = generate_csv_to_download()

            st.markdown(download_link, unsafe_allow_html=True)


if __name__ == '__main__':
    MainPage().execute()
