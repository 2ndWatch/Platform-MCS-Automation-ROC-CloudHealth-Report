from modules import client_selection as cs
from modules import login_config as lcon
from modules import aws_azure_login as aws
from src.banner import banner
from getpass import getpass
import os


def main():
    print(banner)
    print('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')

    username = input('Please enter your 2nd Watch Azure username (ex. aeversmeyer): ')
    password = getpass('Please enter your Azure password [input is hidden]: ')
    lcon.export_username_password(username, password)

    # Profile configuration needs to be changed. Just writing the file apparently doesn't work.
    # Hopefully this isn't a deal-breaker.
    print('Configuring client profiles...')
    clients_dict = lcon.configure_login_credentials()
    print('Client profile configuration complete.\n')

    selected_client, client_keys, clients_to_report = cs.client_selection(clients_dict)

    # TODO: make sure azure_login references clients.txt
    for key in client_keys:
        profile_names = []
        if len(clients_dict[key]['profiles']) > 1:
            # iterate through list of profile_names
            continue
        else:
            logged_in = aws.azure_login(client_keys, clients_dict[key]['profiles'][0]['profile_name'])
            if logged_in:
                print(f'\nYou have been logged into the {selected_client} account.')

    return selected_client, client_keys, clients_to_report


cl, cl_keys, cl_list = main()
print(f'client: {cl}')
print(f'client keys: {cl_keys}')
print(f'client list: {cl_list}')
