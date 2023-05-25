import modules.aws_azure_login as aws
import modules.compare_resources as cr
import modules.create_dataframes as cdf
import modules.get_resources as gr
import modules.login_config as lcfg
import pandas as pd


def create_cost_df(name, date):
    cost_df = pd.read_csv(f'cloudhealth/{name} ebs cost {date}.csv')

    # drop columns so df only has 'ResourceId' and 'Cost'
    cost_df.drop(['PayerAccountId', 'LinkedAccountId', 'RecordType', 'ProductName', 'UsageType', 'Operation',
                  'ItemDescription', 'UsageStartDate', 'SyntheticId'], axis='columns', inplace=True)

    # Reformat ResourceId so that it only displays 'snap-*'
    cost_df['ResourceId'] = cost_df['ResourceId'].apply(lambda x: x[-22:])

    return cost_df


# Log into all accounts for each selected client and run the scripts
def process_clients(clients_dict, client_keys, report_date, three_months, logger):
    for key in client_keys:

        # Create 6 dataframes for the client
        df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps = cdf.create_dataframes()

        df_ebs_cost = create_cost_df(clients_dict[key]['name'], report_date)

        for profile in clients_dict[key]['profiles']:
            profile_name = profile['profile_name']
            lcfg.set_login_credentials(profile, profile_name)

            logger.info(f'\nLogging in to {profile["profile_name"]}. Enter your Azure credentials in '
                        f'the popup window.')
            logged_in = aws.azure_login(profile_name, logger)

            if logged_in:
                logger.info(f'You are logged in to {profile["profile_name"]}.')

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
                return 1

    return 0
