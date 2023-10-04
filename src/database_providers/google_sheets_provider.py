from gspread import service_account, exceptions
import warnings


class GoogleSheetsProvider:
    def __init__(self, cred_filename, link):
        self.database = service_account(filename=cred_filename).open_by_url(link)
        self.sheet = None

    def set_sheet(self, title):
        try:
            self.sheet = self.database.worksheet(title)
        except exceptions.WorksheetNotFound:
            self.sheet = self.database.add_worksheet(title, 0, 0)

    def save(self, data: [[]]):
        warnings.filterwarnings(action="ignore", category=UserWarning)
        self.sheet.update("A1:B{0}".format(len(data)), data)

    def get(self):
        return self.sheet.get_all_values()
