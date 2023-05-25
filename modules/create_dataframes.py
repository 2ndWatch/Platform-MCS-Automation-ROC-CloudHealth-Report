import pandas as pd


def create_dataframes(for_client=False):

    df_eips = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Public IP', 'Cost Per Month'])
    df_oldimages = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                         'Image Id', 'Image Name', 'Image Age', 'Storage Size (GB)',
                                         'Snapshot Count', 'Cost Per Month'])
    df_ebssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                                        'Size (GB)', 'Create Date', 'Image Id', 'Cost Per Month'])
    df_vol = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Volume Id',
                                   'Size (GB)', 'Volume Type', 'Cost Per Month'])
    df_unami = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Image Id',
                                     'Image Name', 'Storage Size (GB)', 'Snapshot Count', 'Cost Per Month'])
    df_rdssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                        'Snapshot Id', 'Allocated Storage (GB)', 'Create Date'])

    if for_client:
        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
        columns_list = [
            ['Account Name', 'Account Number', 'Region Name', 'Public IP', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name',
             'Image Age', 'Storage Size (GB)', 'Snapshot Count', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Size (GB)',
             'Create Date', 'Image Id', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)',
             'Volume Type', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name',
             'Storage Size (GB)', 'Snapshot Count', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
             'Allocated Storage (GB)', 'Create Date']
        ]
        empty_unmatched_row = [
            ['-', '-', '-', 'No resources matched', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-']
        ]
        empty_excluded_row = [
            ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-'],
            ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
            ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-']
        ]
        return df_list, columns_list, empty_unmatched_row, empty_excluded_row

    return df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps


def create_cost_df(name, date):
    cost_df = pd.read_csv(f'cloudhealth/{name} ebs cost {date}.csv')

    # drop columns so df only has 'ResourceId' and 'Cost'
    cost_df.drop(['PayerAccountId', 'LinkedAccountId', 'RecordType', 'ProductName', 'UsageType', 'Operation',
                  'ItemDescription', 'UsageStartDate', 'SyntheticId'], axis='columns', inplace=True)

    # Reformat ResourceId so that it only displays 'snap-*'
    cost_df['ResourceId'] = cost_df['ResourceId'].apply(lambda x: x[-22:])

    return cost_df
