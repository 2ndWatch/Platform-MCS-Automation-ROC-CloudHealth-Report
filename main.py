from modules import process_client as pc
from datetime import datetime, timedelta
from src.banner import banner
import easygui as eg
import json
import sys
import logging

# Initialize the logger
logger = logging.getLogger('2wchval')
logging.basicConfig(level=logging.DEBUG,
                    filename=f'log/2wchval_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.log',
                    filemode='a')
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logger.addHandler(console)

# Read the clients.json file into a dictionary
with open('src/clients.json') as cl:
    cl_txt = cl.read()
clients_dict = json.loads(cl_txt)


# Subtract 90 days from a given date
def convert_date(date_string):
    dt_date = datetime.strptime(date_string, '%Y-%m-%d')
    three_months = timedelta(days=90)
    three_month_dt_date = dt_date - three_months
    three_month_date = datetime.strftime(three_month_dt_date, '%Y-%m-%d')
    return three_month_date


# Primary user interface function
def main(clients):
    print(banner)
    logger.info('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')

    # Welcome message box
    welcome = eg.msgbox('Welcome to the 2nd Watch Cloud Health resource verification program.\n\n'
                        'Click the <Begin> button to proceed.',
                        '2nd Watch Cloud Health Validator', ok_button='Begin')

    # User closed msgbox
    if welcome is None:
        sys.exit(0)

    # Get today's date and transform to three-month date
    today = datetime.now().strftime('%Y-%m-%d')
    three_months = convert_date(today)

    # Create a list of clients from which to select
    choices = []
    for key, value in clients.items():
        choices.append(f'{key}-{value["name"]}')

    while 1:
        selected_clients = eg.multchoicebox('Select one or multiple clients by left-clicking.\n\n'
                                            'Click the <Cancel> button to exit.',
                                            'Client Selection', choices, preselect=None)
        if selected_clients is None:
            sys.exit(0)

        # Create list of client keys from client selection
        client_keys = [choice.split('-')[0] for choice in selected_clients]
        client_names = []
        for choice in selected_clients:
            choice_split = choice.split('-')
            client_name = choice_split[1]
            if len(choice_split) > 2:
                for i in range(2, len(choice_split)):
                    client_name += f' {choice_split[i]}'
            client_names.append(client_name)
        logger.info(f'Client keys: {client_keys}')
        logger.info(f'You are running the program for: {client_names}')

        ready = eg.ccbox(f'You chose to validate Cloud Health policy results for: {client_names}.\n\n'
                         f'You can track validation progress in the console window.\n\n'
                         f'Click the <Run> button to begin resource validation.\n'
                         f'Click the <Exit> button to exit the program without validating any resources.',
                         title='Client Selection Result', choices=['Run', 'Exit'], cancel_choice='Exit')
        if not ready:
            sys.exit(0)

        # Process validation procedure for each client
        process_result = pc.process_clients(clients_dict, client_keys, today, three_months, logger)

        if process_result == 1:

            # No logins were successful
            logger.info('\nNo successful logins recorded. No reports will be generated.\n'
                        f'If you believe this message was generated incorrectly, please report the failure and submit '
                        f'the log file from this run attempt. The log file can be found in the <log> directory.'
                        )

            eg.msgbox(f'No successful logins recorded. No reports will be generated.\n\n'
                      f'If you believe this message was generated incorrectly, please report the failure and submit '
                      f'the log file from this run attempt. The log file can be found in the <log> directory.\n\n'
                      f'Click the <Exit> button to exit the program.',
                      'Resource Validation Result', ok_button='Exit')

        else:

            # At least one login was successful; displays any logins that did not succeed
            logger.info(f'\nValidation is complete.\n\n'
                        f'Accounts not validated: {process_result[0]}\n'
                        f'Clients not validated: {process_result[1]}\n'
                        f'Unauthorized API calls: {process_result[2]}\n\n'
                        f'Reports can be found in the <output> directory. The log file can be '
                        f'found in the <log> directory.')

            eg.msgbox(f'Validation has completed.\n\n'
                      f'Accounts not validated: {process_result[0]}\n'
                      f'Clients not validated: {process_result[1]}\n'
                      f'Unauthorized API calls: {process_result[2]}\n\n'
                      f'Reports can be found in the <output> directory. The log file can be '
                      f'found in the <log> directory.\n\n'
                      f'Please run the program again if you want to validate more clients.\n\n'
                      f'Click the <Exit> button to exit the program.',
                      'Resource Validation Result', ok_button='Exit')

        return


main(clients_dict)
