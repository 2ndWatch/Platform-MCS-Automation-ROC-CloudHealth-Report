import logging

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

    df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]

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

    ch_df_list = [df_ch_eips, df_ch_oldimages, df_ch_ebssnaps, df_ch_vol, df_ch_unami, df_ch_rdssnaps]

    return ch_df_list


def create_column_lists_empty_rows():
    # These are the column labels from the client dataframes
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

    # These match columns from the client dataframes
    empty_unmatched_row = [
        ['-', '-', '-', 'No resources matched', '-'],
        ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources matched', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources matched', '-', '-', '-'],
        ['-', '-', '-', 'No resources matched', '-', '-', '-'],
        ['-', '-', '-', 'No resources matched', '-', '-', '-']
    ]

    # These are the column labels from the Cloud Health reports
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

    # These match columns from the Cloud Health reports
    empty_excluded_row = [
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-'],
        ['-', '-', 'No resources excluded', '-', '-', '-', '-', '-', '-']
    ]

    return columns_list, empty_unmatched_row, columns_ch_list, empty_excluded_row


def create_cost_df(name):
    cost_df = pd.read_csv(f'cloudhealth/{name} ebs cost.csv')

    # Drop columns so df only has 'ResourceId' and 'Cost'
    cost_df.drop(['PayerAccountId', 'LinkedAccountId', 'RecordType', 'ProductName', 'UsageType', 'Operation',
                  'ItemDescription', 'UsageStartDate', 'SyntheticId'], axis='columns', inplace=True)

    # Reformat ResourceId so that it only displays 'snap-*'
    try:
        cost_df['ResourceId'] = cost_df['ResourceId'].apply(lambda x: x[-22:])
    except TypeError:
        cost_df['ResourceId'] = cost_df['ResourceId'].astype(str).apply(lambda x: x[-22:])
    else:
        cost_df['ResourceId'] = cost_df['ResourceId'].astype(str).apply(lambda x: x[-22:])
        logging.critical("Unable to Reformat ResourceId so that it only displays 'snap-*'")

    return cost_df
