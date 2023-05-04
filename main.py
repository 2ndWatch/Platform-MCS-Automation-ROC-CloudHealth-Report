from modules import aws_azure_login as aws

# replace eventually with a function or something to read the clients from some other data source
clients = {
    'a': 'Edmund Optics',
    'b': 'Cypherworx'
}


def main():
    print('\nThis is the Cloud Health resource verification script.\n')
    number_of_clients = input('How many clients do you want to run the script for? Enter:\n'
                              '   a to run for one client\n'
                              '   b to run for multiple clients\n'
                              '   c to run for all clients\n'
                              'Your selection: ')
    if number_of_clients == 'a':
        print('\nSelect a client. Enter:')
        for key, value in clients.items():
            print(f'   {key} for {value}')
        selected_client = input('Your selection: ')
        while selected_client not in clients.keys():
            print(f'\n{selected_client} is not a valid input.')
            selected_client = input('Your selection: ')
        print(f'\nThe script will be run for {clients[selected_client]}.')
    elif number_of_clients == 'b':
        selected_clients = []
        print('\nYou will be able to select multiple clients. But that does not work right now.')
    else:
        print('\nThe script will be run for all clients. But that does not work right now.')


main()

# if __name__ == 'main':
#     main()
