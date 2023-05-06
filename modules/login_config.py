import json
import os


def export_username_password(username, password):
    os.environ['AZURE_DEFAULT_USERNAME'] = username + '@2ndwatch.com'
    os.environ['AZURE_DEFAULT_PASSWORD'] = password

    print('\nUsername and password have been set.')


# This doesn't work. Apparently need to run 'aws_azure_login --configure --profile foo' for each profile.
def configure_login_credentials():
    with open('src/clients.txt') as cl:
        cl_txt = cl.read()

    clients = json.loads(cl_txt)

    with open('src/config', 'w') as conf:
        conf.write('[default] \n \n')

        for key, client in clients.items():
            if len(client['profiles']) > 1:
                for profile in client['profiles']:
                    write_data = [f'[profile {profile["profile_name"]}] \n',
                                  f'azure_tenant_id={profile["tenant_id"]} \n',
                                  f'azure_app_id_uri={profile["app_id_uri"]} \n',
                                  f'azure_default_username={os.environ.get("AZURE_DEFAULT_USERNAME")} \n',
                                  f'azure_default_role_arn= \n',
                                  'azure_default_duration_hours=1 \n',
                                  'azure_default_remember_me=false \n \n']
                    for line in write_data:
                        conf.write(line)
            elif client['profiles']:
                write_data = [f'[profile {client["profiles"][0]["profile_name"]}] \n',
                              f'azure_tenant_id={client["profiles"][0]["tenant_id"]} \n',
                              f'azure_app_id_uri={client["profiles"][0]["app_id_uri"]} \n',
                              f'azure_default_username={os.environ.get("AZURE_DEFAULT_USERNAME")} \n',
                              f'azure_default_role_arn= \n',
                              'azure_default_duration_hours=1 \n',
                              'azure_default_remember_me=false \n \n']
                for line in write_data:
                    conf.write(line)
            else:
                continue

    with open('src/credentials', 'w') as cred:
        cred.write('[default] \n \n')

    os.environ['AWS_CONFIG_FILE'] = 'src/config'
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = 'src/credentials'

    return clients
