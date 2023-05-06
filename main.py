from modules import client_selection as cs
from modules import login_config as lcon
from modules import aws_azure_login as aws
from src.banner import banner
from getpass import getpass


def main():
    print(banner)
    print('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')

    username = input('Please enter your 2nd Watch Azure username (ex. aeversmeyer): ')
    password = getpass('Please enter your Azure password [input is hidden]: ')
    lcon.export_username_password(username, password)

    print('Configuring client profiles...')
    clients_dict = lcon.configure_login_credentials()
    print('Client profile configuration complete.\n')

    client, clients_to_report = cs.client_selection(clients_dict)

    # TODO: make sure azure_login references clients.txt
    for client_name in clients_to_report:
        # TODO: have to figure out which dict item to use based on client_name, using client here doesn't work for
        #  multiple client selection. This also allows passing in a profile name to the azure_login function
        if len(clients_dict[client]['profiles']) > 1:
            # TODO: iterate through each profile in multi-profile clients
            continue
        else:
            logged_in = aws.azure_login(client_name)
            if logged_in:
                print(f'You have been logged into the ')

    return client, clients_to_report


cl, cl_list = main()
print(f'client: {cl}')
print(f'client list: {cl_list}')
