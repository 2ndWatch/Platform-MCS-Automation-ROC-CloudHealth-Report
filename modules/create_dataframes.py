import pandas as pd


def create_dataframes(for_client=False):

    df_eips = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Public IP'])
    df_oldimages = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                         'Image Id', 'Image Name', 'Image Age', 'Storage Size (GB)'])
    df_ebssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                                        'Size (GB)', 'Create Date', 'Image Id'])
    df_vol = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)'])
    df_unami = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Image Id',
                                     'Image Name', 'Storage Size (GB)'])
    df_rdssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                        'Snapshot Id', 'Allocated Storage (GB)', 'Create Date'])

    if for_client:
        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
        columns_list = [
            ['Account Name', 'Account Number', 'Region Name', 'Public IP'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name',
             'Image Age', 'Storage Size (GB)'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Size (GB)', 'Create Date', 'Image Id'],
            ['Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)'],
            ['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Storage Size (GB)'],
            ['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Allocated Storage (GB)', 'Create Date']
        ]
        empty_unmatched_row = [
            ['-', '-', '-', 'No resources matched'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-', '-'],
            ['-', '-', '-', 'No resources matched', '-'],
            ['-', '-', '-', 'No resources matched', '-', '-'],
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
