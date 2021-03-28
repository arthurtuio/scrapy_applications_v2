import pandas as pd

from project_folder.lib.utils import FolderVariables


class TransformOutputInCsv:
    CSV_FILES_FOLDER = FolderVariables.CSV_FILES_FOLDER.value

    def __init__(self, tarifas_parsed_by_grupo_tarifario):
        self.grupo_b_tarifas_list = tarifas_parsed_by_grupo_tarifario["tarifas_grupo_b"]
        self.grupo_a_tarifas_list = tarifas_parsed_by_grupo_tarifario["tarifas_grupo_a"]

    def execute(self):
        self._transform_grupo_b_tarifas_in_df_and_csv()
        # self._transform_grupo_a_tarifas_in_df_and_csv()  # Para implementações Futuras

    def _transform_grupo_b_tarifas_in_df_and_csv(self):
        df = pd.DataFrame(self.grupo_b_tarifas_list)

        print("-> Succesfully created grupo B DataFrame!")

        return self._save_grupo_b_df_as_csv(df)

    def _transform_grupo_a_tarifas_in_df_and_csv(self):
        df = pd.DataFrame(self.grupo_a_tarifas_list)

        print("-> Succesfully created grupo A DataFrame!")

        return self._save_grupo_a_df_as_csv(df)

    def _save_grupo_b_df_as_csv(self, df):
        csv_name = self.CSV_FILES_FOLDER + 'output_grupo_b.csv'

        df.to_csv(csv_name)

        print(f"-> Succesfully created grupo B csv, named: {csv_name}")

    def _save_grupo_a_df_as_csv(self, df):
        csv_name = self.CSV_FILES_FOLDER + 'output_grupo_a.csv'

        df.to_csv(csv_name)

        print(f"-> Succesfully created grupo A csv, named: {csv_name}")
