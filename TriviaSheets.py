import random
from TriviaServices import TriviaServices

# Reference: https://github.com/googleworkspace/python-samples/blob/master/sheets/snippets/spreadsheet_snippets.py

class TriviaSheets(object):
    def __init__(self):
        triviaServices = TriviaServices()
        self.service = triviaServices.get_sheets_service()
    
    def get_rows(self, spreadsheet_id, range_name):
        service = self.service
        # pylint: disable=maybe-no-member
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        return rows