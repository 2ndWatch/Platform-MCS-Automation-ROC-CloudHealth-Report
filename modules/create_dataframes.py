import pandas as pd


def create_dataframes(for_client=False):

    df_eips = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Public IP'])
    df_oldimages = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                         'Image Id', 'Image Name', 'Image Age'])
    df_ebssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name',
                                        'Snapshot Id', 'Create Date', 'Image Id'])
    df_vol = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Volume Id'])
    df_unami = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name'])
    df_rdssnaps = pd.DataFrame(columns=['Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Create Date'])

    if for_client:
        df_list = [df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps]
        return df_list

    return df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps
