from enum import Enum


def base_url():
    return "https://agenciaweb.celesc.com.br/"


class CelescUrls(Enum):
    URL_BASE = base_url()
    URL_AUTENTICACAO = base_url() + "AgenciaWeb/autenticar/autenticar.do"
    URL_PASSWORD = base_url() + "AgenciaWeb/autenticar/validarSenha.do"
    URL_HIST_PAGAMENTO = base_url() + "AgenciaWeb/consultarHistoricoPagto/consultarHistoricoPagto.do"
    URL_LISTA_HIST_FATURAS = base_url() + "AgenciaWeb/consultarHistoricoPagto/listaHistoricoFaturas.jsp?d-1335161-p={}"
