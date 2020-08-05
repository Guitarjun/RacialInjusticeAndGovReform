from __future__ import print_function
import gspread
from google.oauth2 import service_account
from pathlib import Path
import pandas as pd


def ask_local():
    local = input('Would you like to use a local copy of the data? (if no internet connection) (y/n): ')
    if local.strip() == 'y':
        return pd.read_csv('Racial Injustice and Government Reform.csv')
    else:
        print('Fetching data...')
        return load_data()


def load_data():
    SCOPE = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    SERVICE_FILE = 'racialinjusticegovreform-783aecec559a.json'
    SPREADSHEET = 'Racial Injustice and Government Reform (Responses)'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_FILE, scopes=SCOPE)
    gc = gspread.authorize(credentials)
    workbook = gc.open(SPREADSHEET)
    sheet = workbook.sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data

def update_columns(data):


def main():

    data = ask_local()
    """
    print("The following sheets are available")
    for sheet in gc.openall():
        print("{} - {}".format(sheet.title, sheet.id))
    """

    print(type(data))


if __name__ == '__main__':
    main()