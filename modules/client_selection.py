# replace eventually with a function or something to read the clients from some other data source
clients = {
    'a': 'CKE',
    'b': 'Cypherworx',
    'c': 'Edmund Optics',
    'd': 'Utilities International',
    'e': 'VNS Health',
    'done': 'multiple clients',
    None: 'None'
}


def client_selection():
    selected_client = None
    selected_clients = []

    print('\nWelcome to the Cloud Health resource verification program.\n')
    number_of_clients = input('How many clients do you want to run the script for? Enter:\n'
                              '   a to run for one client\n'
                              '   b to run for multiple clients\n'
                              '   c to run for all clients\n'
                              '   or enter "exit" to quit the program.\n'
                              'Your selection: ')
    while number_of_clients not in ['a', 'b', 'c', 'exit']:
        print(f'\n{number_of_clients} is not a valid input.')
        number_of_clients = input('Your selection: ')
    if number_of_clients == 'a':
        print('\nSelect a client. Enter:')
        for key, value in clients.items():
            if key == 'done' or key is None:
                continue
            print(f'   {key} for {value}')
        selected_client = input('Your selection: ')
        while selected_client not in clients.keys():
            print(f'\n{selected_client} is not a valid input.')
            selected_client = input('Your selection: ')
        print(f'\nThe script will be run for:')
        print(f'{clients[selected_client]}')
    elif number_of_clients == 'b':
        selected_clients = []
        selected_client = None
        print('\nSelect a client. Enter:')
        for key, value in clients.items():
            if key == 'done' or key is None:
                continue
            print(f'   {key} for {value}')
        print('   or enter "done" to finish selecting clients.\n')
        while selected_client != 'done':
            selected_client = input('Your selection: ')
            if selected_client != 'done' and selected_client in clients.keys():
                selected_clients.append(clients[selected_client])
            while selected_client != 'done' and selected_client not in clients.keys():
                print(f'\n{selected_client} is not a valid input.')
                selected_client = input('Your selection: ')
        print(f'\nThe script will be run for:')
        for client in selected_clients:
            print(f'{client}')
    elif number_of_clients == 'c':
        selected_client = 'done'
        for key, value in clients.items():
            if key == 'done' or key is None:
                continue
            selected_clients.append(value)
        print('\nThe script will be run for all clients:')
        for client in selected_clients:
            print(client)
    else:
        print('\nYou have quit the program. Goodbye!')

    return clients[selected_client], selected_clients
