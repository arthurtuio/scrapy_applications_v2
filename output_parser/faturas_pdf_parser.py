import tabula
import logging  # depois só trocar os prints por logging.info
from os import listdir

from project_folder.lib.utils import FolderVariables



class FaturasPdfParser:
    def __init__(self):
        self._pdfs_folder = FolderVariables.PDF_DOWNLOADS_FOLDER.value

    def process(self):
        for pdf in self.list_pdfs():
            tabula_loaded_tables = self.load_pdf_in_tabula(pdf)

            self.parse_tabula_tables(tabula_loaded_tables)

    def list_pdfs(self):
        print(f"Dir files: {listdir(self._pdfs_folder)}")
        return listdir(self._pdfs_folder)

    def load_pdf_in_tabula(self, pdf):
        """
        :return: Uma lista de Dataframes criada pelo Tabula.

        Pra UC 2574250 TODAS as listas tem entre 2 ou 3 dfs.
        """
        print(f"-> loading pdf {pdf} ...")

        return tabula.read_pdf(
            input_path=self._pdfs_folder + pdf,
            pages='all',
            multiple_tables=True
        )

    def parse_tabula_tables(self, tabula_loaded_tables):
        #print(f"Len tabula_loaded_tables: {len(tabula_loaded_tables)}")

        self.parse_first_tabula_table(tabula_loaded_tables[0])

        if len(tabula_loaded_tables) == 2:
            # print(" -> Apenas 1 table para fazer o parse")
            pass

        elif len(tabula_loaded_tables) == 3:
            # print(" -> 2 tables para fazer o parse")
            self.parse_second_tabula_table(tabula_loaded_tables[1])

        else:
            print(f" -> Achado algo estranho!! Len tabula_loaded_tables: {len(tabula_loaded_tables)}")

    def parse_first_tabula_table(self, table):
        pass

    def parse_second_tabula_table(self, table):
        pass


if __name__ == '__main__':
    FaturasPdfParser().process()
