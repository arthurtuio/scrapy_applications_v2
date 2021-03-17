"""
Desatualizado.
"""

import pandas as pd
import glob


class XlsParser:
    XLS_FOLDER = "/home/arthur/personal_projects/scrapy_celesc/project_folder/project_folder/downloads/GerarExcel?op=histConsGC/"

    def __init__(self):
        pass

    def execute(self):
        pass

    def load_xls_as_df(self):
        xls_file = glob.glob(self.XLS_FOLDER + "*.xls")[0]
        print(xls_file)
        df = pd.read_excel(xls_file)

        print(df)


if __name__ == '__main__':
    XlsParser().load_xls_as_df()