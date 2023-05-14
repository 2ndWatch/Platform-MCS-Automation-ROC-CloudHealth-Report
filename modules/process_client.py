import modules.aws_azure_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.get_resources as gr
import modules.login_config as lcfg


# Log into all accounts for each selected client and run the scripts
# TODO: This looks awful and is not DRY. Refactor eventually. But for now, it works.
def process_clients(clients_dict, client_keys, report_date, three_months, logger):
    for key in client_keys:

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        if len(clients_dict[key]['profiles']) > 1:
            for profile in clients_dict[key]['profiles']:
                lcfg.set_login_credentials(profile)

                logger.info(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials in '
                            f'the popup window.')
                logged_in = aws.azure_login(logger)

                if logged_in:
                    logger.info(f'You are logged in to {profile["profile_name"]}.')

                if len(profile['region']) > 1:
                    for region in profile['region']:
                        df_eips, df_oldimages, df_ebssnaps, \
                            df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date,
                                                                             three_months, df_eips, df_oldimages,
                                                                             df_ebssnaps, df_vol, df_unami,
                                                                             df_rdssnaps, logger)
                else:
                    region = profile['region'][0]
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                         df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                         df_unami, df_rdssnaps, logger)
        else:
            profile = clients_dict[key]['profiles'][0]
            lcfg.set_login_credentials(profile)

            logger.info(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials '
                        f'in the popup window.')
            logged_in = aws.azure_login(logger)

            if logged_in:
                logger.info(f'You are logged in to {profile["profile_name"]}.')

            if len(profile['region']) > 1:
                for region in profile['region']:
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                         df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                         df_unami, df_rdssnaps, logger)
            else:
                region = profile['region'][0]
                df_eips, df_oldimages, df_ebssnaps, \
                    df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                     df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                     df_unami, df_rdssnaps, logger)

        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
        file_list_csv = cr.create_file_list(clients_dict[key]['name'], report_date)

        logger.info('\nResource details collected. Running Cloud Health report validation...')
        cr.compare_resources(clients_dict[key]['name'], df_list, file_list_csv, report_date, logger)

    return
