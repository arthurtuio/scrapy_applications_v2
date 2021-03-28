from output_parser.transform_pdf_in_txt_file import TransformPdfInTxtFile
from output_parser.faturas_txt_parser import FaturasTxtParser
from output_parser.transform_output_in_df import TransformOutputInCsv


class CorePdfToCsvTransformer:
    @staticmethod
    def execute():
        TransformPdfInTxtFile().execute()
        tarifas_parsed_by_grupo_tarifario = FaturasTxtParser().execute()
        TransformOutputInCsv(tarifas_parsed_by_grupo_tarifario).execute()


if __name__ == '__main__':
    CorePdfToCsvTransformer().execute()
