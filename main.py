from modules import process_client as pc
from datetime import datetime, timedelta
from src.banner import banner
import easygui as eg
import json
import sys
import logging

logger = logging.getLogger('2wchval')
logging.basicConfig(level=logging.DEBUG,
                    filename=f'output/2wchval_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.log',
                    filemode='a')
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logger.addHandler(console)


with open('src/clients.txt') as cl:
    cl_txt = cl.read()
clients_dict = json.loads(cl_txt)


def convert_date(date_string):
    dt_date = datetime.strptime(date_string, '%Y-%m-%d')
    three_months = timedelta(days=90)
    three_month_dt_date = dt_date - three_months
    three_month_date = datetime.strftime(three_month_dt_date, '%Y-%m-%d')
    return three_month_date


def main(clients):
    print(banner)
    logger.info('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')
    # Welcome message box
    welcome = eg.msgbox('Welcome to the 2nd Watch Cloud Health resource verification program.\n\n'
                        'Click the <OK> button to proceed.',
                        '2nd Watch Cloud Health Validator')
    if welcome is None:  # User closed msgbox
        sys.exit(0)

    # Get report date; transform to three-month date and reformat to file date
    # TODO: validate format of date
    date_values = eg.multenterbox('Enter the date of the Cloud Health reports.\n',
                                  'Date Entry',
                                  ['Year (YYYY)', 'Month (MM)', 'Day (DD)'])
    report_date = '-'.join(date_values)
    three_months = convert_date(report_date)
    logger.info(f'Report date entered: {report_date}')
    if report_date is None:  # User closed msgbox
        sys.exit(0)

    # Create a list of clients from which to select
    choices = []
    for key, value in clients.items():
        choices.append(f'{key} {value["name"]}')

    while 1:
        selected_clients = eg.multchoicebox('Select one or multiple clients by left-clicking.\n\n'
                                            'Click the <Cancel> button to exit.',
                                            'Client Selection', choices, preselect=None)
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
        logger.info(f'Client keys: {client_keys}')
        logger.info(f'You are running the program for: {client_names}')

        eg.msgbox(f'You chose: {client_names}.\n\nClick the <OK> button to begin validation.\n\n'
                  f'You can track validation progress in the console window.\n\n'
                  f'The program will close after validation is complete.',
                  'Client Selection Result')

        pc.process_clients(clients_dict, client_keys, report_date, three_months, logger)

        logger.info('\nValidation is complete. Reports and log files can be found in the <output> directory.')

        eg.msgbox(f'Validation has completed. Reports and log files can be found in the <output> directory.\n\n'
                  f'Please run the program again if you want to validate more clients.\n\n'
                  f'Click the <OK> button to exit the program.',
                  'Client Selection Result')

        return


main(clients_dict)
