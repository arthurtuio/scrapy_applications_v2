import scrapy
from project_folder.items import DemoDownloaderItem

# como -> https://coderecode.com/download-files-scrapy/ esse tutorial ensina

from application.database.to_be_implemented.postgres_connector import PostgresConnector
from application.database.to_be_implemented.repository import CredentialsParoquia


def get_first_not_synced_credential_from_db():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        scrapy_paroquia_repository = CredentialsParoquia(pg_conn)

        all_not_synced_credentials = scrapy_paroquia_repository.get_all_not_synced_credentials()

        pg_conn.commit()

    return all_not_synced_credentials[0]


class CelescLoginSpider(scrapy.Spider):
    name = "celesc_post_login"
    start_urls = [
        #'https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/loginCliente.do',
        'https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/autenticar.do'
    ]

    LISTA_PARAMS_UCS = [
        {
            "unidade_consumidora": '10303826',
            "tipo_documento": 'CPJ',
            "numero_doc_cpf": '84708478006010',
            "numero_doc_cpj": '84708478006010',
            "tipo_usuario": 'clienteUnCons',
            "password": 'pfin60',
            "mesInicial": '03',
            "anoInicial": '2019',
            "mesFinal": '03',
            "anoFinal": '2021',
        },
        {
            "unidade_consumidora": '10303826',
            "tipo_documento": 'CPJ',
            "numero_doc_cpf": '84708478006010',
            "numero_doc_cpj": '84708478006010',
            "tipo_usuario": 'clienteUnCons',
            "password": 'pfin60',
            "mesInicial": '03',
            "anoInicial": '2020',
            "mesFinal": '03',
            "anoFinal": '2021',
        },
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.unidade_consumidora = '10303826'
        # self.tipo_documento = "CPJ"
        # self.numero_doc_cpf = self.numero_doc_cpj = '84708478006010'
        # self.tipo_usuario = 'clienteUnCons'
        # self.password = 'pfin60'
        # self.mesInicial = '03'
        # self.anoInicial = '2019'
        # self.mesFinal = '03'
        # self.anoFinal = '2021'
        self.credentials = get_first_not_synced_credential_from_db()

    def start_requests(self):
        requests = []

        for i, account in enumerate(self.LISTA_PARAMS_UCS):
            # request = FormRequest(
            #     'http://example.com/login',
            #   formdata={'form_login_name': account['login'], 'form_pwd_name': account['pwd']},
            #   callback=self.parse,
            #   dont_filter=True
            # )

            # self._uc_params_dict = account
            print(f"account: {account}")

            request = scrapy.Request(
                url='https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/autenticar.do',
                callback=self.parse,
            )

            # request = scrapy.FormRequest(
            #     url='https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/autenticar.do',
            #     formdata={
            #         'sqUnidadeConsumidora': self._uc_params_dict['unidade_consumidora'],
            #         'tpDocumento': self._uc_params_dict['tipo_documento'],
            #         'numeroDocumentoCPF': self._uc_params_dict['numero_doc_cpf'],
            #         'numeroDocumentoCNPJ': self._uc_params_dict['numero_doc_cpj'],
            #         'tipoUsuario': self._uc_params_dict['tipo_usuario']
            #     },
            #     callback=self.parse,
            # )

            request.meta['cookiejar'] = i
            requests.append(request)

        return requests

    def parse(self, response):
        self.log('visitei a página de login: {}'.format(response.url))

        #token = response.css('input[name="csrf_token"]::attr(value)').extract_first()

        # for uc_params_dict in self.LISTA_PARAMS_UCS:
        #
        #     self._uc_params_dict = uc_params_dict

        yield scrapy.FormRequest(
            url='https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/autenticar.do',
            formdata={
                'sqUnidadeConsumidora': self.credentials['unidade_consumidora'],
                'tpDocumento': self.credentials['tipo_documento'],
                'numeroDocumentoCPF': self.credentials['numero_documento'],
                'numeroDocumentoCNPJ': self.credentials['numero_documento'],
                'tipoUsuario': self.credentials['tipo_usuario']
            },
            callback=self.post_password,
            dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']}
        )

    def post_password(self, response):
        self.log('visitei a página de post password: {}'.format(response.url))

        return scrapy.FormRequest(
            url='https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/validarSenha.do',
            formdata={'senha': self.credentials['password_value']},
            callback=self.get_historico_consumo_e_demanda,
            dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']},
        )

    def get_historico_consumo_e_demanda(self, response):
        # open_in_browser(response)

        self.log('visitei a página de consula historico consumo e demanda: {}'.format(response.url))

        base_url = 'https://agenciaweb.celesc.com.br/AgenciaWeb/consultarHistConsGC/histConsGC.do'

        return scrapy.FormRequest(
            url=base_url,#+endpoint,
            formdata={
                'mesInicial': self.credentials['mesinicial'],
                'anoInicial': self.credentials['anoinicial'],
                'mesFinal': self.credentials['mesfinal'],
                'anoFinal': self.credentials['anofinal'],
            },
            callback=self.download_excel,
            dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']},
        )

    def download_excel(self, response):
        # open_in_browser(response)

        url = "https://agenciaweb.celesc.com.br/AgenciaWeb/GerarExcel?op=histConsGC"

        item = DemoDownloaderItem()
        item['file_urls'] = [url]
        return item

    def download_excel_v2(self, response):
        """
        Essa versão tbm talvez funcione, mas a outra é bem mais simples
        """
        # open_in_browser(response)

        self.log('visitei a pagina pra baixar o excel: {}'.format(response.url))

        file_url_xpath = response.xpath(
            '//*[@id="pg"]/table[2]/tbody/tr/td/a' #::attr(href)'
        ).get()

        file_url_xpath = response.urljoin(file_url_xpath)

        item = DemoDownloaderItem()
        item['file_urls'] = [file_url_xpath]
        yield item


# if __name__ == '__main__':
#     print(
#         get_first_not_synced_credential_from_db()
#     )