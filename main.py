from modules import client_selection as cs
from modules import login_config as lcon
from src.banner import banner


def main():
    print(banner)
    print('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')

    is_configured = lcon.are_profiles_configured()

    # move this to login_config? don't entirely love how this works right now, but it works
    if not is_configured:
        configure = input('Client account profiles appear to not be configured. Enter:\n'
                          '   y to configure profiles\n'
                          '   b to bypass profile configuration\n'
                          '   or "exit" to exit the program\n'
                          'Your selection: ')
        while configure not in ['y', 'b', 'exit']:
            print(f'\n{configure} is not a valid input.')
            configure = input('Your selection: ')
        while True:
            if configure == 'b':
                print('\nYou have bypassed profile configuration.\n')
                break
            elif configure == 'y':
                lcon.configure_login_credentials()
                break
            else:
                print('\nYou have exited the program. Goodbye!')
                return None, None
    # end section to move

    client, clients_list = cs.client_selection()

    return client, clients_list


cl, cl_list = main()
# print(f'client: {cl}')
# print(f'client list: {cl_list}')
