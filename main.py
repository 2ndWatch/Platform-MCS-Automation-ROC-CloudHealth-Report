from modules import client_selection as cs
from modules import login_config as lcon
from modules import aws_azure_login as aws
from modules import create_dataframes as cdf
from getresources import get_resources
from src.banner import banner
from getpass import getpass
import json

with open('src/clients.txt') as cl:
    cl_txt = cl.read()
clients_dict = json.loads(cl_txt)

report_date = '2023-04-24'
three_month_cutoff_date = '2023-01-24'


def main(clients):
    print(banner)
    print('\nWelcome to the 2nd Watch Cloud Health resource verification program.\n')

    # Set username and password as environment variables
    username = input('Please enter your 2nd Watch Azure username (ex. aeversmeyer): ')
    password = getpass('Please enter your Azure password [input is hidden]: ')
    lcon.export_username_password(username, password)

    # Return a client name (if applicable), a list of dict keys, and a list of profile names
    selected_client, client_keys = cs.client_selection(clients)

    # Log into all accounts for a client and run the scripts
    # This looks awful and is not DRY. Refactor eventually. But for now, it works.
    for key in client_keys:

        # Create 6 dataframes for the client
        df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        if len(clients_dict[key]['profiles']) > 1:
            for profile in clients_dict[key]['profiles']:
                lcon.set_login_credentials(profile)

                print(f'\nLogging in to {profile["profile_name"]}. Please approve the MFA push notification...')
                logged_in = aws.azure_login()

                if logged_in:
                    print(f'You are logged in to {profile["profile_name"]}.')

                if len(profile['region']) > 1:
                    for region in profile['region']:
                        print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                        get_resources(profile, region, report_date, three_month_cutoff_date,
                                      df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps)
                else:
                    region = profile['region'][0]
                    print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                    get_resources(profile, region, report_date, three_month_cutoff_date,
                                  df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps)
        else:
            profile = clients_dict[key]['profiles'][0]
            lcon.set_login_credentials(profile)

            print(f'\nLogging in to {profile["profile_name"]}. Please approve the MFA push notification...')
            logged_in = aws.azure_login()

            if logged_in:
                print(f'You are logged in to {profile["profile_name"]}.')

            if len(profile['region']) > 1:
                for region in profile['region']:
                    print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                    get_resources(profile, region, report_date, three_month_cutoff_date,
                                  df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps)
            else:
                region = profile['region'][0]
                print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                get_resources(profile, region, report_date, three_month_cutoff_date,
                              df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps)

    return selected_client, client_keys


cl, cl_keys = main(clients_dict)
