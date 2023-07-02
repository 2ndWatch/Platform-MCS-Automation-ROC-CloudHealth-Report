import modules.aws_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.fill_cloudhealth_dataframes as fcd
import modules.get_resources as gr
import modules.generate_final_report as gen
import aws_sso_lib as sso
import boto3


def create_boto3_session(profile, login, start_url, sso_region, role_name, region):
    if login == 'sso':
        account_id = int(profile['account_number'])
        session = sso.get_boto3_session(start_url, sso_region, account_id, role_name, region=region,
                                        login=False, sso_cache=None, credential_cache=None)
    else:
        session = boto3.Session(region_name=region)
    return session


# Log into all accounts for each selected client and run the functions to gather resources
def process_clients(clients_dict, client_keys, today, three_months, logger):
    accounts_logged_in = 0
    accounts_not_logged_in_list = []
    clients_logged_in = 0
    clients_not_logged_in_list = []
    unauthorized_list = []

    for key in client_keys:
        client_name = clients_dict[key]['name']
        login = clients_dict[key]['login']

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        # Create and fill 6 dataframes for the Cloud health data
        filled_ch_dataframes = fcd.fill_cloudhealth_dataframes(client_name, logger)

        # Create EBS cost dataframe
        df_ebs_cost = cdf.create_cost_df(client_name, logger)

        for profile in clients_dict[key]['profiles']:
            logged_in = False
            start_url = None
            sso_region = None
            role_name = None

            if login == 'sso':
                start_url = clients_dict[key]['start_url']
                sso_region = clients_dict[key]['sso_region']
                role_name = clients_dict[key]['role_name']

            # log in to the client
            if login == 'sso' or login == 'aal':
                logged_in = aws.aws_login(login, profile, client_name, logger,
                                          start_url=start_url, sso_region=sso_region)
            else:
                logger.info(f'No login type configured for {client_name}. Skipping this client.')
                clients_not_logged_in_list.append(client_name)

            if logged_in:
                if login == 'sso':
                    clients_logged_in += 1
                else:
                    accounts_logged_in += 1

                # Append data to dataframes for each wasted spend resource for each specified region in an account
                # Currently this is set to all US regions for all accounts
                for region in profile['region']:

                    # TODO: may need to catch an exception if an SSO session can't be made for some reason
                    # create a boto3 session
                    session = create_boto3_session(profile, login, start_url, sso_region, role_name, region)

                    df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, \
                        df_rdssnaps, unauthorized = gr.get_resources(profile, region, session, today,
                                                                     three_months, df_eips, df_oldimages,
                                                                     df_ebssnaps, df_vol, df_unami,
                                                                     df_rdssnaps, df_ebs_cost, logger)

                    for item in unauthorized:
                        unauthorized_list.append(item)

                # Create a list of client dataframes
                filled_client_dataframes = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]

                # Compare resources found by this program against those found by Cloud Health policies
                logger.info('\nResource details collected. Running Cloud Health report validation...')

                cr.compare_resources(client_name, filled_client_dataframes, filled_ch_dataframes, today, logger)

            else:
                if login == 'sso':
                    logger.info(f'You were not logged in, skipping {client_name}.')
                    clients_not_logged_in_list.append(client_name)
                else:
                    logger.info(f'You were not logged in, skipping {profile["profile_name"]}.')
                    accounts_not_logged_in_list.append(profile['profile_name'])
                continue

    logger.debug(f'Did not log into: {accounts_not_logged_in_list}, {clients_not_logged_in_list}')

    if accounts_logged_in == 0 and clients_logged_in == 0:
        logger.debug('\nNo successful logins recorded. No reports will be generated.')

        # Return if no accounts were accessed
        return 1
    else:
        logger.info('\nCreating final reports with overviews...')

        # Create the 'Final' report for SDMs
        gen.generate_final_report(logger)
        return [accounts_not_logged_in_list, clients_not_logged_in_list, unauthorized_list]
