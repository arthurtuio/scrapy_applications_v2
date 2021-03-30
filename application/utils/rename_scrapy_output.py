import glob
import os
import base64
import pandas as pd

from application.variables_names import FolderVariables


PDF_DOWNLOAD_PATH = FolderVariables.PDF_DOWNLOADS_FOLDER.value
CSV_PATH = FolderVariables.CSV_FILES_FOLDER.value
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
            os.rename(file, PDF_DOWNLOAD_PATH + new_file_name)
        except OSError as e:
            print(f"-> Error! Something happened in file {file}:", e)

    print("-> All files successfully renamed and changed to pdf!")


def _list_all_files_without_extension():
    all_files = glob.glob(PDF_DOWNLOAD_PATH + "*")

    all_pdf_files = glob.glob(PDF_DOWNLOAD_PATH + "*" + SELECTED_FORMAT)

    for pdf_file in all_pdf_files:
        all_files.remove(pdf_file)

    return all_files


def count_number_of_pdfs():
    all_pdf_files = glob.glob(PDF_DOWNLOAD_PATH + "*" + SELECTED_FORMAT)
    return {
        "count": len(all_pdf_files),
        "folder": PDF_DOWNLOAD_PATH,
    }


def generate_csv_to_download():
    """Generates a link allowing the data in a given panda dataframe to be downloaded"""

    df = get_output_csv_as_df()

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="output_grupo_b.csv">Download csv file</a>'

    return href


def get_output_csv_as_df():
    csv_obj = CSV_PATH + "output_grupo_b.csv"

    return pd.read_csv(csv_obj)
