from modules import client_selection as cs


def main():
    client, clients_list = cs.client_selection()

    return client, clients_list


cl, cl_list = main()
# print(f'client: {cl}')
# print(f'client list: {cl_list}')
