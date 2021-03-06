import scrapy
from application.variables_names import CelescUrls, FolderVariables

# como -> https://coderecode.com/download-files-scrapy/ esse tutorial ensina

from application.database.g_sheets_hook import GSheetsHook


class CelescLoginSpider(scrapy.Spider):
    name = "celesc_post_login_pdfs"
    start_urls = [
        CelescUrls.URL_AUTENTICACAO.value,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.credentials = GSheetsHook().get_first_not_synced_row()

    def parse(self, response):
        print(f"self.credentials: {self.credentials}")

        self.log('Accessing page: {}'.format(response.url))

        yield scrapy.FormRequest(
            url=CelescUrls.URL_AUTENTICACAO.value,
            formdata={
                'sqUnidadeConsumidora': str(self.credentials['unidade_consumidora']),
                'tpDocumento': self.credentials['tipo_documento'],
                'numeroDocumentoCPF': str(self.credentials['numero_documento']),
                'numeroDocumentoCNPJ': str(self.credentials['numero_documento']),
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
        self.log('Accessing page: {}'.format(response.url))

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
        # open_in_browser(response)

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

        download_folder = FolderVariables.PDF_DOWNLOADS_FOLDER.value

        self.logger.info('-> Saving PDF %s', path)
        with open(
                file=download_folder + "liro_liro_sturt_liro" + str(self.contador_legal),
                mode='wb'
        ) as file:
            file.write(response.body)
