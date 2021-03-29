import streamlit as st

from core_executor import CoreExecutor


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
        ]

        operacao_selecionada = st.sidebar.selectbox("Operação escolhida", lista_operacoes)

        if operacao_selecionada == lista_operacoes[1]:
            self._download_celesc_faturas_as_pdfs()

        elif operacao_selecionada == lista_operacoes[2]:
            self._convert_faturas_to_csv()

    def _download_celesc_faturas_as_pdfs(self):
        # textinho de explicação
        # dar um botao pra pessoa fazer a parada
        # pass
        st.markdown("AAA")
        if st.button("Botão"):
            CoreExecutor(enable_download_from_site=True).execute()

    def _convert_faturas_to_csv(self):
        CoreExecutor().execute()
        # textinho de aplicacao
        # dar um botao pra pessoa fazer a parada
        # disponibilizar a opcao de download


if __name__ == '__main__':
    MainPage().execute()
