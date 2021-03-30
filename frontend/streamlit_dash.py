import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


from utils.rename_scrapy_output import get_output_csv_as_df


class StreamlitDash:
    def __init__(self, input_df=False):
        self.input_df = input_df or get_output_csv_as_df()

    def execute(self):
        self._show_df()
        _PlotlyPlots(self.input_df).execute()

    def _show_df(self):
        st.markdown("** Dataframe **:")
        return st.dataframe(self.input_df)


class _PlotlyPlots:
    def __init__(self, input_df):
        self.input_df = input_df

    def execute(self):
        self.plot_consumo_faturado()
        self.plot_valor_ate_o_vencimento()

    def plot_consumo_faturado(self):
        labels = sorted(self._convert_datas_string_to_datetime(
            self.input_df['Data da leitura atual'].values.tolist()
        ))
        faturado = self.input_df['Consumo faturado no mês'].values.tolist()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=labels,
            y=faturado,
            name="Faturado",
            hovertext="kW"
        ))

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
                    y=0.5,
                    showarrow=False,
                    text="Valores [kW]",
                    textangle=-90,
                    xref="paper",
                    yref="paper"
                )
            ],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            autosize=True,
            margin=dict(b=100),
            title_text=f"Demanda Faturada",
            xaxis_tickangle=-60,
            height=600, width=900,
        )

        return st.plotly_chart(fig)

    def plot_valor_ate_o_vencimento(self):
        labels = sorted(self._convert_datas_string_to_datetime(
            self.input_df['Data da leitura atual'].values.tolist()
        ))
        faturado = self.input_df['VALOR ATÉ O VENCIMENTO'].values.tolist()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=labels,
            y=faturado,
            name="Faturado",
            hovertext="kW"
        ))

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
                    y=0.5,
                    showarrow=False,
                    text="Valores [kW]",
                    textangle=-90,
                    xref="paper",
                    yref="paper"
                )
            ],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            autosize=True,
            margin=dict(b=100),
            title_text=f"VALOR ATÉ O VENCIMENTO",
            xaxis_tickangle=-60,
            height=600, width=900,
        )

        return st.plotly_chart(fig)

    @staticmethod
    def _convert_datas_string_to_datetime(lista_de_strings_contendo_datas):
        return [
            datetime.strptime(string, ' %d/%m/%Y')
            for string in lista_de_strings_contendo_datas
        ]

    # def _numero_dias_faturados_plot(self):
    #     fig = px.bar(
    #         self.input_df,
    #         x='Número de dias faturados',
    #         y='Leitura atual',
    #         height=400,
    #         autosize=True,
    #     )
    #     fig.show()

