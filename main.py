from modules import process_client as pc
from datetime import datetime, timedelta
from src.banner import banner
import easygui as eg
import json
import sys

with open('src/clients.txt') as cl:
    cl_txt = cl.read()
clients_dict = json.loads(cl_txt)


def convert_date(date_string):
    dt_date = datetime.strptime(date_string, '%Y-%m-%d')
    three_months = timedelta(days=90)
    three_month_dt_date = dt_date - three_months
    three_month_date = datetime.strftime(three_month_dt_date, '%Y-%m-%d')
    ch_file_date = datetime.strftime(dt_date, '%m-%d-%Y')
    if ch_file_date.startswith('0'):
        ch_file_date = ch_file_date[1:]
    return three_month_date, ch_file_date


def main(clients):
    # Welcome message box
    welcome = eg.msgbox('Welcome to the 2nd Watch Cloud Health resource verification program.\n\n'
                        'Click the <OK> button to proceed.',
                        '2nd Watch Cloud Health Validator')
    print(banner)
    print('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')
    if welcome is None:  # User closed msgbox
        sys.exit(0)

    # Get report date; transform to three-month date and reformat to file date
    # TODO: validate format of date
    date_values = eg.multenterbox('Enter the date of the Cloud Health reports.\n',
                                  'Date Entry',
                                  ['Year (YYYY)', 'Month (MM)', 'Day (DD)'])
    report_date = '-'.join(date_values)
    three_months, file_date = convert_date(report_date)
    print(f'Report date entered: {report_date}')
    if report_date is None:  # User closed msgbox
        sys.exit(0)

    # Create a list of clients from which to select
    msg = ""
    title = "Client Selection"
    choices = []
    for key, value in clients.items():
        if key == 'done' or key == 'None':
            continue
        print(f'   {key} for {value["name"]}')
        choices.append(f'{key} {value["name"]}')

    while 1:
        selected_clients = eg.multchoicebox('Select one or multiple clients by left-clicking.\n\n'
                                            'Click the <Cancel> button to exit.',
                                            title, choices, preselect=None)
        if selected_clients is None:
            sys.exit(0)

        # Create list of client keys from client selection
        client_keys = [choice.split(' ')[0] for choice in selected_clients]
        client_names = []
        for choice in selected_clients:
            choice_split = choice.split(' ')
            client_name = choice_split[1]
            if len(choice_split) > 2:
                for i in range(2, len(choice_split)):
                    client_name += f' {choice_split[i]}'
            client_names.append(client_name)
        print(f'Client keys: {client_keys}')
        print(f'You are running the program for: {client_names}')

        eg.msgbox(f'You chose: {client_names}.\n\nClick the <OK> button to begin validation.\n\n'
                  f'You can track validation progress in the console window.',
                  'Client Selection Result')

        pc.process_clients(clients_dict, client_keys, report_date, three_months, file_date)

        eg.msgbox(f'Validation has been performed for {client_names}.\n\n'
                  f'Output files can be found in the <outputs> directory.\n\n'
                  f'If more validations are needed, please run the program again.\n\n'
                  f'Click the <OK> button to exit the program.',
                  'Validation Successful')

        return client_keys


cl_keys = main(clients_dict)
