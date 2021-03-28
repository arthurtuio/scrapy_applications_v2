from tika import parser

from project_folder.lib.utils import FolderVariables
from project_folder.lib.os_glob_utils import list_all_dir_files


class TransformPdfInTxtFile:
    PDF_DOWNLOADS_FOLDER = FolderVariables.PDF_DOWNLOADS_FOLDER.value
    TXT_FILES_FOLDER = FolderVariables.TXT_FILES_FOLDER.value

    def execute(self):
        print("Initiated TransformPdfInTxtFile...")

        for pdf in self._get_all_pdfs():
            pdf_content = self._get_pdf_content_using_tika(pdf)
            self._transform_pdf_in_txt(pdf, pdf_content)
            print(f"-> Successfully transformed follwing pdf in txt: {pdf}")

    def _get_all_pdfs(self):
        return list_all_dir_files(self.PDF_DOWNLOADS_FOLDER)

    def _get_pdf_content_using_tika(self, pdf):
        result = parser.from_file(self.PDF_DOWNLOADS_FOLDER + pdf)
        return result["content"]

    def _transform_pdf_in_txt(self, pdf, pdf_content):
        file_name = self.TXT_FILES_FOLDER + pdf

        with open(file_name, "w") as fp:
            return fp.writelines(pdf_content)


if __name__ == '__main__':
    TransformPdfInTxtFile().execute()
