from project_folder.lib.regras_negocio_grupo_b import (
    DADOS_MEDICAO_DICT,
    HISTORICO_CONSUMO_ENERG_ELET_DICT,
    N_DA_UNIDADE_CONSUMIDORA_DICT,
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
        dados_do_faturamento = self._parse_dados_do_faturamento()
        composicao_precos = self._parse_composicao_precos()

        # print(dados_do_faturamento)

        output = {
            **dados_medicao,
            **hist_cons_ener_elet,
            **dados_unidade_consumidora,
            **dados_do_faturamento,
            **composicao_precos,
        }

        self._standarize_output(output)

        return output

    def _parse_dados_medicao(self):
        dados_medicao = DADOS_MEDICAO_DICT()

        full_payload_splited_by_newline = self._split_payload_by_newline(remove_blank_lines=True)

        for line in full_payload_splited_by_newline:
            for key in dados_medicao.keys():
                if key in line:
                    splitted_line = line.split(":")
                    # print(splitted_line)
                    dados_medicao[key] = splitted_line[1] if len(splitted_line) > 1 else None

        return dados_medicao

    def _parse_historico_consumo_energ_elet(self):
        full_payload_splited_by_newline = self._split_payload_by_newline()

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

        full_payload_splited_by_newline = self._split_payload_by_newline(remove_blank_lines=True)
        # print(full_payload_splited_by_newline)

        for index, line in enumerate(full_payload_splited_by_newline):
            for key in dados_unidade_consumidora.keys():
                if key == line:
                    # print(line)
                    # print(full_payload_splited_by_newline[index + 1])
                    # print("####")

                    dados_unidade_consumidora[key] = full_payload_splited_by_newline[index + 1]

        return dados_unidade_consumidora

    def _parse_dados_do_faturamento(self):
        dados_do_faturamento = {}

        full_payload_splited_by_newline = self._split_payload_by_newline(remove_blank_lines=True)

        alphabetic_params = []

        for index, line in enumerate(full_payload_splited_by_newline):
            if line == "Lançamentos e Serviços":
                alphabetic_params = self._check_how_many_params_exist(full_payload_splited_by_newline, index)

        for param in alphabetic_params:
            for index, line in enumerate(full_payload_splited_by_newline):
                if param == line:
                    dados_do_faturamento[param] = full_payload_splited_by_newline[index + len(alphabetic_params)]

        #print(dados_do_faturamento)
        return dados_do_faturamento

    def _parse_composicao_precos(self):
        composicao_precos = {}

        full_payload_splited_by_newline = self._split_payload_by_newline(remove_blank_lines=True)

        for index, line in enumerate(full_payload_splited_by_newline):
            for key in COMPOSICAO_PRECO_DICT().keys():
                if key == line:
                    composicao_precos[key] = full_payload_splited_by_newline[index + 1]

        # print(composicao_precos)
        return composicao_precos

    def _split_payload_by_newline(self, remove_blank_lines=False):
        splitted_payload = self.full_payload.split("\n")

        if remove_blank_lines:
            splitted_payload = [line for line in splitted_payload if line is not '']

        return splitted_payload

    @staticmethod
    def _check_how_many_params_exist(full_payload_splited_by_newline, index):
        """
        Vai do 2 até 6, por exemplo:
            full_payload_splited_by_newline[index + 2] = Consumo
            full_payload_splited_by_newline[index + 3] = Correcao Monetaria por Atraso 06/2016
            full_payload_splited_by_newline[index + 4] = Juros Conta Anterior 06/2016
            full_payload_splited_by_newline[index + 5] = Multa Conta Anterior 06/2016
            full_payload_splited_by_newline[index + 6] = Cosip
        """
        alphabetic_params = []

        if full_payload_splited_by_newline[index + 2].split(" ")[0].isalpha():
            alphabetic_params.append(full_payload_splited_by_newline[index + 2])

        if full_payload_splited_by_newline[index + 3].split(" ")[0].isalpha():
            alphabetic_params.append(full_payload_splited_by_newline[index + 3])

        if full_payload_splited_by_newline[index + 4].split(" ")[0].isalpha():
            alphabetic_params.append(full_payload_splited_by_newline[index + 4])

        if full_payload_splited_by_newline[index + 5].split(" ")[0].isalpha():
            alphabetic_params.append(full_payload_splited_by_newline[index + 5])

        if full_payload_splited_by_newline[index + 6].split(" ")[0].isalpha():
            alphabetic_params.append(full_payload_splited_by_newline[index + 6])

        #print(alphabetic_params)
        return alphabetic_params

    @staticmethod
    def _standarize_output(output):
        add_correcao_monetaria = False
        add_juros_conta_anterior = False
        add_multa_conta_anterior = False

        for key in output.keys():
            if "Correcao Monetaria por Atraso" in key:
                add_correcao_monetaria = key
                #print(f"add_correcao_monetaria: {add_correcao_monetaria}")

            if "Juros Conta Anterior" in key:
                add_juros_conta_anterior = key
                #print(f"add_juros_conta_anterior: {add_juros_conta_anterior}")

            if "Multa Conta Anterior" in key:
                add_multa_conta_anterior = key
                #print(f"add_multa_conta_anterior: {add_multa_conta_anterior}")

        if add_correcao_monetaria:
            output["Correcao Monetaria por Atraso Valor"] = output[add_correcao_monetaria]
            output["Correcao Monetaria por Atraso Data"] = add_correcao_monetaria.split(" ")[4]
            output.pop(add_correcao_monetaria)

        if add_juros_conta_anterior:
            output["Juros Conta Anterior Valor"] = output[add_juros_conta_anterior]
            output["Juros Conta Anterior Data"] = add_juros_conta_anterior.split(" ")[3]
            output.pop(add_juros_conta_anterior)

        if add_multa_conta_anterior:
            output["Multa Conta Anterior Valor"] = output[add_multa_conta_anterior]
            output["Multa Conta Anterior Data"] = add_multa_conta_anterior.split(" ")[3]
            output.pop(add_multa_conta_anterior)

        if output.get("Consumo"):
            output["Consumo Faturado"] = output["Consumo"][0]
            output["Consumo Tarifa (R$)"] = output["Consumo"][1]
            output["Consumo Valor (R$)"] = output["Consumo"][2]
            output.pop("Consumo")

        return output

