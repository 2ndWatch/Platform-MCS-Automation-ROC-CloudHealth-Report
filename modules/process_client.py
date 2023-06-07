import modules.aws_azure_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.fill_cloudhealth_dataframes as fcd
import modules.get_resources as gr
import modules.login_config as lcfg
import modules.generate_final_report as gen


# Log into all accounts for each selected client and run the functions to gather resources
def process_clients(clients_dict, client_keys, today, three_months, logger):
    accounts_logged_in = 0
    accounts_not_logged_in = 0
    accounts_not_logged_in_list = []

    for key in client_keys:
        client_name = clients_dict[key]['name']

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        # Create and fill 6 dataframes for the Cloud health data
        filled_ch_dataframes = fcd.fill_cloudhealth_dataframes(client_name, logger)

        # Create EBS cost dataframe
        df_ebs_cost = cdf.create_cost_df(client_name)

        for profile in clients_dict[key]['profiles']:
            profile_name = profile['profile_name']

            # Set certain aws-azure-login environmental variables - still needed
            lcfg.set_login_credentials(profile, profile_name)

            logger.info(f'\nLogging in to {profile_name}. Enter your Azure credentials in '
                        f'the popup window.')

            # Log into an account (a 'profile') using aws-azure-login
            logged_in = aws.azure_login(profile_name, logger)

            # Get resources and compare to Cloud Health data if successfully logged in; otherwise, skip the profile
            if logged_in:
                logger.info(f'You are logged in to {profile_name}.')
                accounts_logged_in += 1

                # Append data to dataframes for each wasted spend resource for each specified region in an account
                # Currently this is set to all US regions for all accounts
                for region in profile['region']:
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, today,
                                                                         three_months, df_eips, df_oldimages,
                                                                         df_ebssnaps, df_vol, df_unami,
                                                                         df_rdssnaps, df_ebs_cost, logger)

                # Create a list of client dataframes
                filled_client_dataframes = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]

                # Compare resources found by this program against those found by Cloud Health policies
                logger.info('\nResource details collected. Running Cloud Health report validation...')

                cr.compare_resources(client_name, filled_client_dataframes, filled_ch_dataframes, today, logger)
            else:
                logger.info(f'You were not logged in, skipping {profile["profile_name"]}.')
                accounts_not_logged_in += 1
                accounts_not_logged_in_list.append(profile['profile_name'])
                continue

    logger.debug(f'Did not log into: {accounts_not_logged_in_list}')

    if accounts_not_logged_in > 0 and accounts_logged_in == 0:
        logger.debug('\nNo successful logins recorded. No reports will be generated.')

        # Return if no accounts were accessed
        return 1
    else:
        logger.info('\nCreating final reports with overviews...')

        # Create the 'Final' report for SDMs
        gen.generate_final_report(logger)
        return accounts_not_logged_in_list
