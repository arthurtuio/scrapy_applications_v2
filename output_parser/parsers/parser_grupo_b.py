from project_folder.lib.regras_negocio_grupo_b import (
    DADOS_MEDICAO_DICT,
    HISTORICO_CONSUMO_ENERG_ELET_DICT,
    N_DA_UNIDADE_CONSUMIDORA_DICT,
    DADOS_DO_FATURAMENTO_DICT,
    LANCAMENTOS_E_SERVICOS_DICT,
    COMPOSICAO_PRECO_DICT,
)


class ParserGrupoB:
    def __init__(self, payload):
        self.full_payload = payload["all_content"]
        self.payload_lines_list = payload["lines"]

    def execute(self):
        dados_medicao = self._parse_dados_medicao()
        hist_cons_ener_elet = self._parse_historico_consumo_energ_elet()
        dados_unidade_consumidora = self._parse_n_da_unidade_consumidora()

        # print(dados_medicao)
        print(dados_unidade_consumidora)

    def _parse_dados_medicao(self):
        dados_medicao = DADOS_MEDICAO_DICT()

        for line in self.payload_lines_list:
            for key in dados_medicao.keys():
                if key in line:
                    splitted_line = line.split(":")
                    # print(splitted_line)
                    dados_medicao[key] = splitted_line[1] if len(splitted_line) > 1 else None

        return dados_medicao

    def _parse_historico_consumo_energ_elet(self):  # aqui eu preciso tratar com bastante carinho
        full_payload_splited_by_newline = self.full_payload.split("\n")

        hist_cons_ener_elet_with_dates_keys = {}

        for index, line in enumerate(full_payload_splited_by_newline):
            for key in HISTORICO_CONSUMO_ENERG_ELET_DICT().keys():
                if key == line:
                    # print(line)
                    # print(full_payload_splited_by_newline[index + 2])
                    # print("####")

                    hist_cons_ener_elet_with_dates_keys[line] = full_payload_splited_by_newline[index + 2]

        return hist_cons_ener_elet_with_dates_keys

    def _parse_n_da_unidade_consumidora(self):
        dados_unidade_consumidora = N_DA_UNIDADE_CONSUMIDORA_DICT()

        full_payload_splited_by_newline = self.full_payload.split("\n")

        for index, line in enumerate(full_payload_splited_by_newline):
            for key in dados_unidade_consumidora.keys():
                if key in line:
                    # print(line)
                    # print(full_payload_splited_by_newline[index + 2])
                    # print("####")

                    dados_unidade_consumidora[key] = full_payload_splited_by_newline[index + 2]

        return dados_unidade_consumidora
