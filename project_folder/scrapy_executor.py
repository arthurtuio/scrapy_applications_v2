import os
import time
from scrapy.settings import Settings
from project_folder.spiders.celesc_post_login_pdfs import CelescLoginSpider
from scrapy.crawler import CrawlerProcess

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from database.postgres_connector import PostgresConnector
from database.repository import CredentialsParoquia
from database.g_sheets_hook import GSheetsHook


from output_parser.rename_scrapy_output import rename_scrapy_output_based_in_credentials


def execute_scrapy():
    """
    Solucao criada usando essas refs:
    - https://stackoverflow.com/questions/25170682/running-scrapy-from-script-not-including-pipeline
    - https://stackoverflow.com/questions/32984597/scrapy-attributeerror-settings-object-has-no-attribute-update-settings
    """
    spider = CelescLoginSpider  # Infelizmente não posso chamar a classe passando nada de param de entrada :(
    settings = Settings()
    print(f"settings: {settings}")

    os.environ['SCRAPY_SETTINGS_MODULE'] = 'project_folder.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')

    process = CrawlerProcess(settings)

    process.crawl(spider)
    process.start()


#    raise error.ReactorNotRestartable()
#    twisted.internet.error.ReactorNotRestartable
    # -> Corrigir esse erro assim> https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable


class CoreScrapyExecutor:
    def __init__(self):
        self._scrapy_paroquia_repository = None

    def execute(self):
        first_not_synced_credential = GSheetsHook().get_first_not_synced_row()

        execute_scrapy()
        self._rename_output_based_on_credentials(first_not_synced_credential)

        GSheetsHook().update_selected_row(first_not_synced_credential)

    @staticmethod
    def _rename_output_based_on_credentials(credential):
        rename_scrapy_output_based_in_credentials(credential)


if __name__ == '__main__':
    CoreScrapyExecutor().execute()
