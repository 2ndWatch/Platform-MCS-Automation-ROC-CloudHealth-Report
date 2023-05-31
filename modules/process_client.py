import modules.aws_azure_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.get_resources as gr
import modules.login_config as lcfg
import modules.generate_final_report as gen


# Log into all accounts for each selected client and run the scripts
def process_clients(clients_dict, client_keys, report_date, three_months, logger):
    accounts_logged_in = 0
    accounts_not_logged_in = 0
    accounts_not_logged_in_list = []
    for key in client_keys:

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()
        # Create EBS cost dataframe
        df_ebs_cost = cdf.create_cost_df(clients_dict[key]['name'], report_date)

        for profile in clients_dict[key]['profiles']:
            profile_name = profile['profile_name']
            lcfg.set_login_credentials(profile, profile_name)

            logger.info(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials in '
                        f'the popup window.')
            logged_in = aws.azure_login(profile_name, logger)

            if logged_in:
                logger.info(f'You are logged in to {profile["profile_name"]}.')
                accounts_logged_in += 1

                for region in profile['region']:
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date,
                                                                         three_months, df_eips, df_oldimages,
                                                                         df_ebssnaps, df_vol, df_unami,
                                                                         df_rdssnaps, df_ebs_cost, logger)

                df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
                file_list_csv = cr.create_file_list(clients_dict[key]['name'], report_date)

                logger.info('\nResource details collected. Running Cloud Health report validation...')
                cr.compare_resources(clients_dict[key]['name'], df_list, file_list_csv, report_date, logger)
            else:
                logger.info(f'You were not logged in, skipping {profile["profile_name"]}.')
                accounts_not_logged_in += 1
                accounts_not_logged_in_list.append(profile['profile_name'])
                continue

    logger.debug(f'Did not log into: {accounts_not_logged_in_list}')
    if accounts_not_logged_in > 0 and accounts_logged_in == 0:
        print(f'Not logged in: {accounts_not_logged_in}; logged in: {accounts_logged_in}')
        logger.debug('\nNo successful logins recorded. No reports will be generated.')
        return 1
    else:
        logger.info('\nCreating final reports with overviews...')
        gen.generate_final_report(logger)
        return accounts_not_logged_in_list
