import os
from enum import Enum


home_folder = os.getcwd()


def _base_url():
    return "https://agenciaweb.celesc.com.br/"


def _base_project_folder():
    return home_folder + "/personal_projects/clone_scrapy_celesc_v2/scrapy_applications_v2/"


class GSheetsUtils(Enum):
    SERVICE_ACCOUNT_JSON_CREDENTIALS_FILE_LOCATION = home_folder + "/autonomus-gide-5aa74b8c0202.json"
    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1X3fLRluAt0QSKVdo_GHFo0-Fi0bQvWbRR2rOElPa5OI/edit#gid=0"


class CelescUrls(Enum):
    """
    Não precisa ser editado
    """
    URL_BASE = _base_url()
    URL_AUTENTICACAO = _base_url() + "AgenciaWeb/autenticar/autenticar.do"
    URL_PASSWORD = _base_url() + "AgenciaWeb/autenticar/validarSenha.do"
    URL_HIST_PAGAMENTO = _base_url() + "AgenciaWeb/consultarHistoricoPagto/consultarHistoricoPagto.do"
    URL_LISTA_HIST_FATURAS = _base_url() + "AgenciaWeb/consultarHistoricoPagto/listaHistoricoFaturas.jsp?d-1335161-p={}"
    
    
class FolderVariables(Enum):
    """
    Precisa ser editado de acordo com seu ambiente
    """
    PDF_DOWNLOADS_FOLDER = _base_project_folder() + "project_folder/downloads/"
    SPIDERS_FOLDER = _base_project_folder() + "project_folder/spiders"
    TXT_FILES_FOLDER = _base_project_folder() + "application/files/txt_files/"
    CSV_FILES_FOLDER = _base_project_folder() + "application/files/csv_files/"