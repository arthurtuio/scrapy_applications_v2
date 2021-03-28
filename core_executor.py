from project_folder.scrapy_executor import CoreScrapyExecutor
from output_parser.core_pdf_to_csv_transformer import CorePdfToCsvTransformer


class CoreExecutor:
    def __init__(
            self,
            enable_download_from_site=False,
            enable_transform_in_csv=False,
            enable_upload_in_cloud=False
    ):
        self.enable_download_from_site = enable_download_from_site
        self.enable_transform_in_csv = enable_transform_in_csv
        self.enable_upload_in_cloud = enable_upload_in_cloud

    def execute(self):
        if self.enable_download_from_site:
            CoreScrapyExecutor().execute()

        if self.enable_transform_in_csv:
            CorePdfToCsvTransformer().execute()


if __name__ == '__main__':
    CoreExecutor().execute()
