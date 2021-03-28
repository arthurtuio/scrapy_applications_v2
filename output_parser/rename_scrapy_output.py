import glob
import os

from utils import FolderVariables


DOWNLOAD_PATH = FolderVariables.PDF_DOWNLOADS_FOLDER.value
SELECTED_FORMAT = ".pdf"


def rename_scrapy_output_based_in_credentials(credentials):

    print("Renaming and fixing scrapy output files types to pdf...")

    alias_paroquia = credentials["alias_paroquia"]
    uc = str(credentials["unidade_consumidora"])

    index = 0
    for file in _list_all_files_without_extension():
        index += 1

        new_file_name = alias_paroquia + "__" + uc + "_" + str(index) + SELECTED_FORMAT

        try:
            os.rename(file, DOWNLOAD_PATH + new_file_name)
        except OSError as e:
            print(f"-> Error! Something happened in file {file}:", e)

    print("-> All files successfully renamed and changed to xls!")


def _list_all_files_without_extension():
    all_files = glob.glob(DOWNLOAD_PATH + "*")

    all_pdf_files = glob.glob(DOWNLOAD_PATH + "*" + SELECTED_FORMAT)

    for pdf_file in all_pdf_files:
        all_files.remove(pdf_file)

    return all_files

