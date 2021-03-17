import glob
import os

download_path = "/home/arthur/personal_projects/scrapy_celesc/project_folder/project_folder/downloads/GerarExcel?op=histConsGC/"


def rename_scrapy_output_based_in_credentials(credentials):
    print("Renaming and fixing scrapy output files types to xls...")

    uc = credentials["unidade_consumidora"]
    data_inicial = credentials["mesinicial"] + "_" + credentials["anoinicial"]
    data_final = credentials["mesfinal"] + "_" + credentials["anofinal"]

    new_file_name = uc + "_" + data_inicial + "__" + data_final + ".xls"

    for file in _list_all_files_without_extension():
        try:
            os.rename(file, download_path + new_file_name)
        except OSError as e:
            print(f"-> Error! Something happened in file {file}:", e)

    print("-> All files successfully renamed and changed to xls!")


def _list_all_files_without_extension():
    all_files = glob.glob(download_path + "*")

    all_csv_files = glob.glob(download_path + "*.xls")

    for csv_file in all_csv_files:
        all_files.remove(csv_file)

    return all_files

