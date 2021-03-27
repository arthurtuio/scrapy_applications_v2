from enum import Enum


def _base_url():
    return "https://agenciaweb.celesc.com.br/"


def _base_project_folder():
    return "/home/arthur/personal_projects/clone_scrapy_celesc_v2/scrapy_applications_v2/"


class CelescUrls(Enum):
    URL_BASE = _base_url()
    URL_AUTENTICACAO = _base_url() + "AgenciaWeb/autenticar/autenticar.do"
    URL_PASSWORD = _base_url() + "AgenciaWeb/autenticar/validarSenha.do"
    URL_HIST_PAGAMENTO = _base_url() + "AgenciaWeb/consultarHistoricoPagto/consultarHistoricoPagto.do"
    URL_LISTA_HIST_FATURAS = _base_url() + "AgenciaWeb/consultarHistoricoPagto/listaHistoricoFaturas.jsp?d-1335161-p={}"
    
    
class FolderVariables(Enum):
    PDF_DOWNLOADS_FOLDER = _base_project_folder() + "project_folder/downloads/"
    SPIDERS_FOLDER = _base_project_folder() + "project_folder/spiders"
    TXT_FILES_FOLDER = _base_project_folder() + "files/txt_files/"
