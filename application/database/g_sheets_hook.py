# referencias:
#   https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#   https://github.com/burnash/gspread

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from application.variables_names import GSheetsUtils


class GSheetsHook:
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
        filename=GSheetsUtils.SERVICE_ACCOUNT_JSON_CREDENTIALS_FILE_LOCATION.value,
        scopes=GSheetsUtils.SCOPES.value
    )

    def get_first_not_synced_row(self):
        print("Getting first not synced credential...")

        for row in self._get_all_rows():
            if row["sync_status"] == 'FALSE':

                print("-> Successfully retrieved first not synced credential!")
                return row

    def update_selected_row(self, row):
        sheet = self._get_sheet_object()

        cell = sheet.find(str(row["id"]))
        cell_row = str(cell.row)

        sync_status_col = "H"
        cell_position = sync_status_col + cell_row

        sync_status_new_value = "TRUE"

        sheet.update(
            cell_position,
            sync_status_new_value
        )

        print(f"-> Successfully updated sheet cell {cell_position} sync_status to 'TRUE'!")

    def _get_all_rows(self):
        return self._get_sheet_object().get_all_records()

    def _get_sheet_object(self):
        client = self._authorize_credentials()
        sheet = client.open_by_url(GSheetsUtils.SHEET_URL.value).sheet1
        return sheet

    def _authorize_credentials(self):
        return gspread.authorize(self.CREDENTIALS)


if __name__ == '__main__':
    hook = GSheetsHook()
    hook.update_selected_row(
        hook.get_first_not_synced_row()
    )
    

