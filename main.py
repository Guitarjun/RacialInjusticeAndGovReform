import gspread
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Use django templates
# TODO: STORE FILES AND DOWNLOADS


def ask_local():
    """
    According to user's response, fetches data from Google API or uses local copy of the dataset
    :return: DataFrame of responses
    """
    local = input('Would you like to use a local copy of the data? (if no internet connection) (y/n): ')
    if local.strip() == 'y':
        return pd.read_csv('data/Racial Injustice and Government Reform.csv')
    else:
        try:
            return load_data()
        except Exception as e:
            print(SystemExit(e))
            print('Could not retrieve data \nUsing local data instead')
            return pd.read_csv('data/Racial Injustice and Government Reform.csv')


def load_data():
    """
    :return: DataFrame of responses
    """
    print('Authenticating...')
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    service_file = 'C:/Users/arjun/Documents/CompSci/racialinjusticegovreform/racialinjusticegovreform-783aecec559a.json'
    print('Fetching data...')
    spreadsheet = 'Racial Injustice and Government Reform (Responses)'
    credentials = service_account.Credentials.from_service_account_file(
        service_file, scopes=scope)
    gc = gspread.authorize(credentials)
    # gc.login()  IN CASE OAUTH 2.0 CREDENTIALS EXPIRE
    workbook = gc.open(spreadsheet)
    sheet = workbook.sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data


def update_columns(data: pd.DataFrame):
    """
    Updates the data set specifically
    :param data: DataFrame of responses
    :return: DataFrame with updated column names
    """
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
    data['race'].replace(to_replace='Indian/Pakistani (Asian subcontinent)', value='South Asian/Indian Subcontinent',
                         inplace=True)
    # data.replace({1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}, inplace=True)


def main():
    # Formatting data
    data = ask_local()
    update_columns(data)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # print(data.to_string())

    # Plotting Bar Graphs
    sns.set(style='whitegrid')
    fig, ax = plt.subplots(1, figsize=(15, 8))

    fig.suptitle('Order and Freedom')
    ax = sns.countplot(data=data, x='order_necessity', palette="ch:.24")
    ax.set_xlabel('(Strongly Disagree) 1 - 5 (Strongly Agree)')
    ax.set_ylabel('Responses: ' + str(len(data['order_necessity'])))
    ax.set_title('It is necessary for the government to preserve order and the rule of law during times of civil '
                 'unrest (even if it means violating individual rights and the Constitution): ')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
    fig.tight_layout(pad=3.0)
    fig.savefig('Bar Graphs.png')


if __name__ == '__main__':
    main()
