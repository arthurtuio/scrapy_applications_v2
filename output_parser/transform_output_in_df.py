import pandas as pd

from project_folder.lib.utils import FolderVariables


class TransformOutputInCsv():
    CSV_FILES_FOLDER = FolderVariables.CSV_FILES_FOLDER.value

    def __init__(self, tarifas_parsed_by_grupo_tarifario):
        self.grupo_b_tarifas_list = tarifas_parsed_by_grupo_tarifario["tarifas_grupo_b"]
        self.grupo_a_tarifas_list = tarifas_parsed_by_grupo_tarifario["tarifas_grupo_a"]

    def transform_grupo_b_tarifas_in_df(self):
        print(f"self.grupo_b_tarifas_list: {self.grupo_b_tarifas_list}")
        df = pd.DataFrame(self.grupo_b_tarifas_list)

        return self._save_df_as_csv(df)

    def _save_df_as_csv(self, df):
        csv_name = 'output.csv'

        print(self.CSV_FILES_FOLDER + csv_name)

        return df.to_csv(self.CSV_FILES_FOLDER + csv_name)



