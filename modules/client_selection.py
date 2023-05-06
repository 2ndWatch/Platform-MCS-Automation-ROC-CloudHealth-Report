def client_selection(clients):
    selected_client = 'None'
    client_keys = []
    selected_clients = []

    number_of_clients = input('How many clients do you want to run the script for? Enter:\n'
                              '   a to run for one client\n'
                              '   b to run for multiple clients\n'
                              '   c to run for all clients\n'
                              '   or enter "exit" to exit the program.\n'
                              'Your selection: ')
    while number_of_clients not in ['a', 'b', 'c', 'exit']:
        print(f'\n{number_of_clients} is not a valid input.')
        number_of_clients = input('Your selection: ')
    if number_of_clients == 'a':
        print('\nSelect a client. Enter:')
        for key, value in clients.items():
            if key == 'done' or key == 'None':
                continue
            print(f'   {key} for {value["name"]}')
        selected_client = input('Your selection: ')
        while selected_client not in clients.keys():
            print(f'\n{selected_client} is not a valid input.')
            selected_client = input('Your selection: ')
        print(f'\nThe script will be run for:')
        print(f'{clients[selected_client]["name"]}')
        client_keys.append(selected_client)
        # TODO: assess if selected_clients list is no longer needed
        selected_clients.append(clients[selected_client]["name"])
    elif number_of_clients == 'b':
        selected_client = 'None'
        print('\nSelect a client. Enter:')
        for key, value in clients.items():
            if key == 'done' or key == 'None':
                continue
            print(f'   {key} for {value["name"]}')
        print('   or enter "done" to finish selecting clients.\n')
        while selected_client != 'done':
            selected_client = input('Your selection: ')
            if selected_client != 'done' and selected_client in clients.keys():
                client_keys.append(selected_client)
                # maybe no longer needed
                selected_clients.append(clients[selected_client]["name"])
            while selected_client != 'done' and selected_client not in clients.keys():
                print(f'\n{selected_client} is not a valid input.')
                selected_client = input('Your selection: ')
        print(f'\nThe script will be run for:')
        for client in selected_clients:
            print(f'{client}')
    elif number_of_clients == 'c':
        selected_client = 'done'
        for key, value in clients.items():
            if key == 'done' or key == 'None':
                continue
            client_keys.append(selected_client)
            # maybe no longer needed
            selected_clients.append(value["name"])
        print('\nThe script will be run for all clients:')
        for client in selected_clients:
            print(client)
    else:
        print('\nYou have exited the program. Goodbye!')

    return clients[selected_client]["name"], client_keys, selected_clients
