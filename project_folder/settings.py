# Scrapy settings for project_folder project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os

#from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from application.variables_names import FolderVariables

settings = get_project_settings()

#settings = Settings()
os.environ['SCRAPY_SETTINGS_MODULE'] = 'project_folder.settings'  #
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')


BOT_NAME = 'project_folder'

SPIDER_MODULES = ['project_folder.spiders']
NEWSPIDER_MODULE = 'project_folder.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'project_folder (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'project_folder.middlewares.ProjectFolderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'project_folder.middlewares.ProjectFolderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'project_folder.pipelines.ProjectFolderPipeline': 300,
#}
ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,  # original
    # 'project_folder.items.DemoDownloaderItem': 1  # o que eu criei pra substituir
    'scrapy_save_as_pdf.pipelines.SaveAsPdfPipeline': -1,
}

FILES_STORE = FolderVariables.PDF_DOWNLOADS_FOLDER.value

# # save-as-pdf: https://github.com/etng/scrapy-save-as-pdf
# PROXY = ""
# CHROME_DRIVER_PATH ='/snap/bin/chromium.chromedriver'
# PDF_SAVE_PATH = "./pdfs"
# PDF_SAVE_AS_PDF = False
# PDF_DOWNLOAD_TIMEOUT = 60
# PDF_PRINT_OPTIONS = {
#     'landscape': False,
#     'displayHeaderFooter': False,
#     'printBackground': True,
#     'preferCSSPageSize': True,
# }
# WEBDRIVER_HUB_URL = 'http://127.0.0.1:4444/wd/hub'


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
