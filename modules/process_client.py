import modules.aws_azure_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.get_resources as gr
import modules.login_config as lcfg


# Log into all accounts for each selected client and run the scripts
# TODO: This looks awful and is not DRY. Refactor eventually. But for now, it works.
def process_clients(clients_dict, client_keys, report_date, three_months):
    for key in client_keys:

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        if len(clients_dict[key]['profiles']) > 1:
            for profile in clients_dict[key]['profiles']:
                lcfg.set_login_credentials(profile)

                print(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials in '
                      f'the popup window.')
                logged_in = aws.azure_login()

                if logged_in:
                    print(f'You are logged in to {profile["profile_name"]}.')

                if len(profile['region']) > 1:
                    for region in profile['region']:
                        print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                        df_eips, df_oldimages, df_ebssnaps, \
                            df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date,
                                                                             three_months, df_eips, df_oldimages,
                                                                             df_ebssnaps, df_vol, df_unami,
                                                                             df_rdssnaps)
                else:
                    region = profile['region'][0]
                    print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                         df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                         df_unami, df_rdssnaps)
        else:
            profile = clients_dict[key]['profiles'][0]
            lcfg.set_login_credentials(profile)

            print(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials in the popup window.')
            logged_in = aws.azure_login()

            if logged_in:
                print(f'You are logged in to {profile["profile_name"]}.')

            if len(profile['region']) > 1:
                for region in profile['region']:
                    print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                    df_eips, df_oldimages, df_ebssnaps, \
                        df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                         df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                         df_unami, df_rdssnaps)
            else:
                region = profile['region'][0]
                print(f'\nRunning resource script for {profile["profile_name"]} in {region}...')
                df_eips, df_oldimages, df_ebssnaps, \
                    df_vol, df_unami, df_rdssnaps = gr.get_resources(profile, region, report_date, three_months,
                                                                     df_eips, df_oldimages, df_ebssnaps, df_vol,
                                                                     df_unami, df_rdssnaps)

        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
        file_list_csv = cr.create_file_list(clients_dict[key]['name'], report_date)

        cr.compare_resources(clients_dict[key]['name'], df_list, file_list_csv, report_date)

    return
