import time

import requests
import scrapy
from project_folder.items import DemoDownloaderItem
from project_folder.lib.celesc_urls import CelescUrls
from scrapy.utils.response import open_in_browser

from scrapy.crawler import CrawlerProcess

from scrapy.pipelines.files import FilesPipeline  # no método file_path dessa classe que eu crio o nome do arquivo.
# como -> https://coderecode.com/download-files-scrapy/ esse tutorial ensina

from database.postgres_connector import PostgresConnector
from database.repository import CredentialsParoquia


def get_first_not_synced_credential_from_db():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        scrapy_paroquia_repository = CredentialsParoquia(pg_conn)

        all_not_synced_credentials = scrapy_paroquia_repository.get_all_not_synced_credentials()

        pg_conn.commit()

    return all_not_synced_credentials[0]


class CelescLoginSpider(scrapy.Spider):
    name = "celesc_post_login_pdfs"
    start_urls = [
        CelescUrls.URL_AUTENTICACAO.value,
    ]

    # LISTA_PARAMS_UCS = [
    #     {
    #         "unidade_consumidora": '10303826',
    #         "tipo_documento": 'CPJ',
    #         "numero_doc_cpf": '84708478006010',
    #         "numero_doc_cpj": '84708478006010',
    #         "tipo_usuario": 'clienteUnCons',
    #         "password": 'pfin60',
    #         "mesInicial": '03',
    #         "anoInicial": '2019',
    #         "mesFinal": '03',
    #         "anoFinal": '2021',
    #     },
    #     {
    #         "unidade_consumidora": '10303826',
    #         "tipo_documento": 'CPJ',
    #         "numero_doc_cpf": '84708478006010',
    #         "numero_doc_cpj": '84708478006010',
    #         "tipo_usuario": 'clienteUnCons',
    #         "password": 'pfin60',
    #         "mesInicial": '03',
    #         "anoInicial": '2020',
    #         "mesFinal": '03',
    #         "anoFinal": '2021',
    #     },
    # ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.credentials = get_first_not_synced_credential_from_db()

    # def start_requests(self):
    #     requests = []
    #
    #     for i, account in enumerate(self.LISTA_PARAMS_UCS):
    #         print(f"account: {account}")
    #
    #         request = scrapy.Request(
    #             url=CelescUrls.URL_AUTENTICACAO.value,
    #             callback=self.parse,
    #         )
    #
    #         request.meta['cookiejar'] = i
    #         requests.append(request)
    #
    #     return requests

        # request = scrapy.Request(
        #     url=CelescUrls.URL_AUTENTICACAO.value,
        #     callback=self.parse,
        # )
        #
        # self.log("Successfully Scraped pages!")
        # return request

    def parse(self, response):
        self.log('Accessing page: {}'.format(response.url))

        yield scrapy.FormRequest(
            url=CelescUrls.URL_AUTENTICACAO.value,
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
        self.log('Accessing page: {}'.format(response.url))

        yield scrapy.FormRequest(
            url=CelescUrls.URL_PASSWORD.value,
            formdata={'senha': self.credentials['password_value']},
            callback=self.get_historico_pagto,
            dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']},
        )

    def get_historico_pagto(self, response):
        """
        Tenho que acessar via href mesmo.
        :param response:
        :return:
        """
        self.log('Accessing page: {}'.format(response.url))

        # pages_list = [1, 2, 3, 4, 5, 6]  # no max ultimos 60 meses, coisa do site da celesc
        #
        # base_url = CelescUrls.URL_LISTA_HIST_FATURAS.value

        # pagination_url = "listaHistoricoFaturas.jsp?d-1335161-p={}"

        # for page in pages_list:
        #     #completed_url = base_url + "/" + pagination_url.format(page)
        #     #print(f"->>- completed_url: {completed_url}")
        #
        #     print(f"->>- base_url.format(page): {base_url.format(page)}")
        #
        #     return scrapy.Request(
        #         url=base_url.format(page),
        #         callback=self.download_pdf,
        #         # dont_filter=True,
        #     # meta={'cookiejar': response.meta['cookiejar']},
        #     )

        return scrapy.Request(
            url=CelescUrls.URL_HIST_PAGAMENTO.value,
            callback=self.paginate_in_historico_pagto,
            dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']},
        )

    def paginate_in_historico_pagto(self, response):

        pages_list = [1, 2, 3, 4, 5, 6]  # no max ultimos 60 meses, coisa do site da celesc

        base_url = CelescUrls.URL_LISTA_HIST_FATURAS.value

        for page in pages_list:
            self.log('Page number {}, url: {}'.format(page, response.url))

            print(f"->>- base_url.format(page): {base_url.format(page)}")

            yield scrapy.Request(
                url=base_url.format(page),
                callback=self.download_pdf,
                # dont_filter=True,
            # meta={'cookiejar': response.meta['cookiejar']},
            )

    def download_pdf(self, response):
        open_in_browser(response)

        pdfs_url = "//body/div/div/div[3]/table[2]//tr[6]//table/tbody/tr/following::td[2]/a[contains(@href, 'imprimirSegundaVia')]"

        print(f"response.xpath(pdfs_url): {response.xpath(pdfs_url)}")

        for link in response.xpath(pdfs_url):
            print(f"link type: {type(link)}")
            print(f"link: {link}")

            relative_url = link.xpath(".//@href").extract_first()
            print(f"relative_url: {relative_url}")
            print(f"type relative_url: {type(relative_url)}")

            self.relative_url = relative_url

            self.absolute_url = "https://agenciaweb.celesc.com.br" + relative_url

            print(f"absolute_url antes do replace: {self.absolute_url}")

            self.absolute_url = self.absolute_url.replace("imprimirSegundaVia.do", "exibirFat.do")

            print(f"absolute_url depois do replace: {self.absolute_url}")

            self.contador_legal = 0

            yield scrapy.Request(
                self.absolute_url,
                self.save_webpage_as_pdf
            )

    def save_webpage_as_pdf(self, response):
        path = response.url
        print(f"path: {response.url}")

        self.contador_legal += 1

        download_folder = "/home/arthur/personal_projects/scrapy_celesc/project_folder/project_folder/downloads/"

        self.logger.info('-> Saving PDF %s', path)
        with open(
                file=download_folder + "liro_liro_sturt_liro" + str(self.contador_legal),
                mode='wb'
        ) as file:
            file.write(response.body)
