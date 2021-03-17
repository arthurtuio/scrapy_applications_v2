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

    time.sleep(10)


class ScrapyExecutor:
    def __init__(self, pg_conn=None):
        self.pg_conn = pg_conn or PostgresConnector().connect_using_localhost_credentials()
        self._scrapy_paroquia_repository = None

    def execute(self):
        with self.pg_conn as pg_conn:
            self._scrapy_paroquia_repository = CredentialsParoquia(pg_conn)

            for credential in self._get_all_not_synced_credentials():
                print(f"-> credential: {credential}")
                execute_scrapy()
                self._update_first_not_synced_credential()
                # self._rename_output_based_on_credentials(credential)

            pg_conn.commit()

    def _get_all_not_synced_credentials(self):
        print("Getting all not synced credentials...")

        credentials = self._scrapy_paroquia_repository.get_all_not_synced_credentials()

        print(f"-> Number of not synced credentials: {len(credentials)}")

        return credentials

    def _update_first_not_synced_credential(self):
        self._scrapy_paroquia_repository.sync_first_not_synced_credential()

    @staticmethod
    def _rename_output_based_on_credentials(credential):
        rename_scrapy_output_based_in_credentials(credential)


    # def _select_first_credential_not_synced(self):
    #     credentials_list = credentials()
    #
    #     filtered_credentials_list = [d for d in credentials_list if d['sync_status'] is False]
    #     return filtered_credentials_list[0]
    #     # print(filtered_credentials_list)
    #     # return filtered_credentials_list


if __name__ == '__main__':
    ScrapyExecutor().execute()
