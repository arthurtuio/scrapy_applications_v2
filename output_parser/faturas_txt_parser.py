from project_folder.lib.utils import FolderVariables
from project_folder.lib.os_glob_utils import list_all_dir_files
from output_parser.parsers.parser_grupo_b import ParserGrupoB
from output_parser.parsers.parser_grupo_a4 import ParserGrupoA4

from output_parser.transform_output_in_df import TransformOutputInCsv


class FaturasTxtParser:
    TXT_FILES_FOLDER = FolderVariables.TXT_FILES_FOLDER.value

    def execute(self):
        faturas_list = []
        
        for fatura in self._load_faturas():
            # print("####")
            # print(fatura)
            content = self._get_fatura_content(fatura)
            grupo_tarifario = self._categorize_in_grupo_tarifario(content)
            
            faturas_list.append({
                "content": content,
                "grupo_tarifario": grupo_tarifario
            })

        tarifas_parsed_by_grupo_tarifario = self._parse_according_to_grupo_tarifario(faturas_list)

        TransformOutputInCsv(tarifas_parsed_by_grupo_tarifario).transform_grupo_b_tarifas_in_df()

    def _load_faturas(self):
        return list_all_dir_files(self.TXT_FILES_FOLDER)

    def _get_fatura_content(self, fatura):
        fp = open(self.TXT_FILES_FOLDER + fatura, "r")
        lines = fp.readlines()

        fp = open(self.TXT_FILES_FOLDER + fatura, "r")
        all_content = fp.read()

        return {
            "all_content": all_content,
            "lines": lines,
        }

    @staticmethod
    def _categorize_in_grupo_tarifario(content):
        if "GRUPO A4" in content["all_content"]:
            return {"grupo_tensao": "A4"}

        elif "Grupo de Tensão: B" and "Tarifa: Convencional" in content["all_content"]:
            return {"grupo_tensao": "B"}

        else:
            print("ERRO!")

    @staticmethod
    def _parse_according_to_grupo_tarifario(faturas_list):
        tarifas_grupo_b = []
        tarifas_grupo_a = []
        
        for fatura in faturas_list:
            content = fatura["content"]
            grupo_tarifario = fatura["grupo_tarifario"]
    
            if grupo_tarifario["grupo_tensao"] == "B":
                tarifas_grupo_b.append(
                    ParserGrupoB(content).execute()
                )
    
            elif grupo_tarifario["grupo_tensao"] == "A4":
                tarifas_grupo_a.append(
                    ParserGrupoA4(content).execute()
                )
    
            else:
                raise Exception

        return {
            "tarifas_grupo_b": tarifas_grupo_b,
            "tarifas_grupo_a": tarifas_grupo_a
        }


if __name__ == '__main__':
    print(
        FaturasTxtParser().execute()
    )

    FaturasTxtParser().execute()
