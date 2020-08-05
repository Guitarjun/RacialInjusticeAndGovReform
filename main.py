from __future__ import print_function
import gspread
from google.oauth2 import service_account
from pathlib import Path
import pandas as pd


def main():
    SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    SERVICE_FILE = 'C:/Users/arjun/Documents/CompSci/racialinjusticegovreform-783aecec559a.json'
    SPREADSHEET = 'Racial Injustice and Government Reform (Responses)'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_FILE, scopes=SCOPE)

    gc = gspread.authorize(credentials)
    print("The following sheets are available")
    for sheet in gc.openall():
        print("{} - {}".format(sheet.title, sheet.id))
    workbook = gc.open(SPREADSHEET)

    sheet = workbook.sheet1

    data = pd.DataFrame(sheet.get_all_records())

    print(data.columns)



if __name__ == '__main__':
    main()