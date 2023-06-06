import pandas as pd


def create_dataframes(for_client=False):
    # Create empty dataframes with desired column names
    df_eips = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Public IP', 'Cost Per Month'])
    df_oldimages = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                         'Image Id', 'Image Name', 'Public', 'Image Age', 'Cost Per Month'])
    df_ebssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                                        'Size (GB)', 'Create Date', 'Image Id', 'Cost Per Month'])
    df_vol = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Volume Id',
                                   'Size (GB)', 'Volume Type', 'Cost Per Month'])
    df_unami = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Image Id',
                                     'Image Name', 'Public', 'Cost Per Month'])
    df_rdssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                        'Snapshot Id', 'Instance Id', 'Allocated Storage (GB)', 'Create Date'])

    # Define variables to be used if a Cloud Health .csv file does not exist
    if for_client:
        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]

        # These should match the columns defined in the dataframes above
        columns_list = [
            ['Account Name', 'Account Number', 'Region Name', 'Public IP', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Public',
             'Image Age', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Size (GB)',
             'Create Date', 'Image Id', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)',
             'Volume Type', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Public', 'Cost Per Month'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Instance Id',
             'Allocated Storage (GB)', 'Create Date']
        ]

        # 'No resources matched' lines up with resource IDs; every other column needs a corresponding '-'
        empty_unmatched_row = [
            ['-', '-', '-', 'No resources matched', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-']
        ]

        # This should not need to be changed; these match columns from the Cloud Health reports
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


def create_cloudhealth_dataframes():
    # Create empty dataframes with desired column names
    df_ch_eips = pd.DataFrame(columns=['New?', 'Account Name', 'Public IP', 'Region Name', 'Instance Name', 'Domain',
                                       'Private IP Address', 'Tags', 'Unattached At'])
    df_ch_oldimages = pd.DataFrame(columns=['New?', 'Account Name', 'Image Id', 'Image Name', 'Root Device Type',
                                            'Public', 'Region Name', 'Image Age'])
    df_ch_ebssnaps = pd.DataFrame(columns=['New?', 'Account Name', 'Snapshot Name', 'Snapshot Id', 'Volume Name',
                                           'Size (GB)', 'Region Name', 'Create Date', 'Snapshot Age'])
    df_ch_vol = pd.DataFrame(columns=['New?', 'Account Name', 'Volume Name', 'Volume Id', 'Instance Name', 'Zone Name',
                                      'Size (GB)', 'In Use', 'List Price Per Month', 'Owner Email',
                                      'Unattached Volumes'])
    df_ch_unami = pd.DataFrame(columns=['New?', 'Account Name', 'Image Id', 'Image Name', 'Root Device Type', 'Public',
                                        'Region Name', 'Instance Count'])
    df_ch_rdssnaps = pd.DataFrame(columns=['New?', 'Account Name', 'Snapshot Id', 'Instance Id', 'Size (GB)',
                                           'Zone Name', 'Create Date', 'Tags', 'Snapshot Age'])

    df_ch_list = [df_ch_eips, df_ch_oldimages, df_ch_ebssnaps, df_ch_vol, df_ch_unami, df_ch_rdssnaps]

    # These should match the columns defined in the dataframes above
    columns_ch_list = [
        ['New?', 'Account Name', 'Public IP', 'Region Name', 'Instance Name', 'Domain', 'Private IP Address',
         'Tags', 'Unattached At'],
        ['New?', 'Account Name', 'Image Id', 'Image Name', 'Root Device Type', 'Public', 'Region Name', 'Image Age'],
        ['New?', 'Account Name', 'Snapshot Name', 'Snapshot Id', 'Volume Name', 'Size (GB)', 'Region Name',
         'Create Date', 'Snapshot Age'],
        ['New?', 'Account Name', 'Volume Name', 'Volume Id', 'Instance Name', 'Zone Name', 'Size (GB)', 'In Use',
         'List Price Per Month', 'Owner Email', 'Unattached Volumes'],
        ['New?', 'Account Name', 'Image Id', 'Image Name', 'Root Device Type', 'Public', 'Region Name',
         'Instance Count'],
        ['New?', 'Account Name', 'Snapshot Id', 'Instance Id', 'Size (GB)', 'Zone Name', 'Create Date', 'Tags',
         'Snapshot Age']
    ]

    # This should not need to be changed; these match columns from the Cloud Health reports
    empty_excluded_ch_row = [
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-']
    ]

    return df_ch_eips, df_ch_oldimages, df_ch_ebssnaps, df_ch_vol, df_ch_unami, df_ch_rdssnaps, \
        columns_ch_list, empty_excluded_ch_row


def create_cost_df(name, date):
    cost_df = pd.read_csv(f'cloudhealth/{name} ebs cost {date}.csv')

    # Drop columns so df only has 'ResourceId' and 'Cost'
    cost_df.drop(['PayerAccountId', 'LinkedAccountId', 'RecordType', 'ProductName', 'UsageType', 'Operation',
                  'ItemDescription', 'UsageStartDate', 'SyntheticId'], axis='columns', inplace=True)

    # Reformat ResourceId so that it only displays 'snap-*'
    cost_df['ResourceId'] = cost_df['ResourceId'].apply(lambda x: x[-22:])

    return cost_df
