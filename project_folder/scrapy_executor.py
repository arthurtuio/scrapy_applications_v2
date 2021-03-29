import os
#from project_folder.settings import Settings # antes era from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from project_folder.spiders.celesc_post_login_pdfs import CelescLoginSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner

from database.g_sheets_hook import GSheetsHook

from output_parser.rename_scrapy_output import rename_scrapy_output_based_in_credentials


import time
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
import os



def _sleep(_, duration=5):
    print(f'sleeping for: {duration}')
    time.sleep(duration)  # block here


def execute_scrapy():
    """
    Solucao criada usando essas refs:
    - https://stackoverflow.com/questions/25170682/running-scrapy-from-script-not-including-pipeline
    - https://stackoverflow.com/questions/32984597/scrapy-attributeerror-settings-object-has-no-attribute-update-settings
    """

    spider = CelescLoginSpider  # Infelizmente não posso chamar a classe passando nada de param de entrada :(

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    def f(q):
        try:

            runner = CrawlerRunner()
            d = runner.crawl(spider)
            d.addBoth(_sleep)
            d.addBoth(lambda _: reactor.stop())
            reactor.run()  # the script will block here until the crawling is finished
            q.put(None)

        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


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
