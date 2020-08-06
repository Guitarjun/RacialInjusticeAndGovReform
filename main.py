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
        try:
            return load_data()
        except:
            print('Could not retrieve data \n Using local data instead')
            return pd.read_csv('Racial Injustice and Government Reform.csv')



def load_data():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    service_file = 'racialinjusticegovreform-783aecec559a.json'
    spreadsheet = 'Racial Injustice and Government Reform (Responses)'
    credentials = service_account.Credentials.from_service_account_file(
                  service_file, scopes=scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open(spreadsheet)
    sheet = workbook.sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data


def update_columns(data: pd.DataFrame):
    column_names = {'Timestamp': 'timestamp',
                    'What is your age?': 'age',
                    'What is your ethnicity/race? ': 'race',
                    'How do you identify yourself (gender)?': 'gender',
                    'What is your religious standing?': 'religion',
                    'Do you identify with one of the two major political parties? If so, please select one:': 'party',
                    'It is necessary for the government to preserve order and the rule of law during times of civil '
                    'unrest (even if it means violating individual rights and the Constitution)': 'order_necessity',
                    'The rule of law is more important than individual freedoms': 'law_importance',
                    'The decision of President Trump to deploy tear gas against peaceful demonstrators (for his photo '
                    'op at St. Johns Episcopal Church) is justified': 'gas_peaceful',
                    'The current militarization of police in the US is necessary': 'militarization_necessity',
                    'Law enforcement officers should be given leniency for acting on impulse (e.g. "I feared for my '
                    'life")': 'cop_leniency',
                    'Law enforcement officers should face more severe penalties for murder (due to their ability to '
                    'legally wield more firepower)': 'cop_penalties',
                    'How do you feel about the statement "All Cops are Bastards" (ACAB)?': 'acab',
                    'Is the US police system in need of systematic reform?': 'reform',
                    'The government should treat the peaceful demonstrators separately from the destructive '
                    'rioters/looters when using force': 'separate_peaceful',
                    'Do you think President Trump has handled the widespread protests effectively?': 'trump_effective',
                    'Social media activism is helpful (not including donations)': 'social_media_helpful',
                    'What have you contributed to this social movement so far?': 'contributions',
                    'Do you think you will care equally about current sociopolitical issues and activism after the '
                    'social media hype is dead?': 'care_posthype',
                    'I am part of a systematically oppressed group in the US': 'oppressed',
                    'Have you had a run-in with the police/other authority that YOU feel was racially motivated?': 'racist_cop',
                    '"White privilege" is real': 'whites_privileged',
                    ' "A riot is the language of the unheard." - MLK': 'mlk_correct',
                    'We should be:': 'color_sensitivity',
                    'Additional thoughts (if you would like to add onto any one of your responses or clarify your '
                    'thoughts on any question)': 'clarification',
                    'Do you consent to having your responses included in any analyses of the data?': 'consent'
                    }
    data.rename(columns=column_names, inplace=True)
    # data['timestamp'] = pd.to_datetime(data['timestamp'])
    # Fix timestamp ^


def main():
    data = ask_local()
    update_columns(data)
    """
    print("The following sheets are available")
    for sheet in gc.openall():
        print("{} - {}".format(sheet.title, sheet.id))
    """
    print(data.columns)


if __name__ == '__main__':
    main()