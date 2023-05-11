from modules import create_dataframes as cdf
from UliPlot.XLSX import auto_adjust_xlsx_column_width as adjust
import pandas as pd


# TODO: date transform to proper format for files
def create_file_list(name, date):
    file_list = [
        f'{name} Elastic IPs_Wasted Spend_unattached over 4 weeks_{date}.xlsx',
        f'{name} EC2 Image_Wasted Spend_older than 3 months_{date}.xlsx',
        f'{name} EC2 Snapshots_Wasted Spend_Older than 3 months_{date}.xlsx',
        f'{name} EBS Volumes_Wasted Spend_unattached over 4 weeks_{date}.xlsx',
        f'{name} EC2 Image_Wasted Spend_not associated_{date}.xlsx',
        f'{name} RDS Snapshots_Wasted Spend_older than 3 months_ {date}.xlsx'
    ]

    return file_list


def fill_empty_df(df_list, excluded_df, empty_unmatched_row, empty_excluded_row, i):
    for df in df_list:
        if df.empty:
            print('   Empty dataframe, adding "No resources unmatched" entry.')
            df.loc[len(df)] = empty_unmatched_row[i]
    if excluded_df.empty:
        try:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            print(excluded_df)
            print(empty_excluded_row[i])
            excluded_df.loc[len(excluded_df)] = empty_excluded_row[i]
        except ValueError:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            excluded_df.loc[len(excluded_df)] = empty_unmatched_row[i]
    return df_list[0], df_list[1], excluded_df


def compare_resources(client_name, df_list, file_list, date):
    column_names = ['Public IP', 'Image Id', 'Snapshot Id', 'Volume Id', 'Image Id', 'Snapshot Id']
    metric_list = ['Unassociated-Elastic-IPs', 'Old-AMIs', 'Old-EBS-Snapshots', 'Unattached-Volumes',
                   'Unused-AMIs', 'Old-RDS-Aurora-Snapshots']
    client_df_list, empty_unmatched_row, empty_excluded_row = cdf.create_dataframes(for_client=True)

    for i in range(6):
        client_df = df_list[i]
        print(f'client df types:\n{client_df.dtypes}')
        file = file_list[i]
        # print(file)
        column_name = column_names[i]
        resource_metric = metric_list[i]

        try:
            cloudhealth_df = pd.read_excel(f'cloudhealth/{file}', "in")
            # print(f'cloudhealth df types:\n{cloudhealth_df.dtypes}')
        except FileNotFoundError:
            print('File not found, creating placeholder dataframe instead...')
            cloudhealth_df = client_df_list[i]

        client_resource_ids = set(client_df[column_name])
        cloudhealth_resource_ids = set(cloudhealth_df[column_name])

        # find the intersection of the two sets of resource ids (i.e. the matching ones)
        matching_resource_ids = cloudhealth_resource_ids.intersection(client_resource_ids)

        # create new dataframes for matched, unmatched, and excluded resource ids
        matched_df = client_df[client_df[column_name].isin(matching_resource_ids)]
        unmatched_df = client_df[~client_df[column_name].isin(matching_resource_ids)]
        excluded_df = cloudhealth_df[~cloudhealth_df[column_name].isin(matching_resource_ids)]

        # Add a 'No resources' row to any empty dataframes
        new_df_list = [matched_df, unmatched_df]
        matched_df_checked, unmatched_df_checked, excluded_df_checked = fill_empty_df(new_df_list,
                                                                                      excluded_df,
                                                                                      empty_unmatched_row,
                                                                                      empty_excluded_row,
                                                                                      i)

        # save the dataframes to a new Excel file
        with pd.ExcelWriter(f'{client_name}-{resource_metric}-Matching-{date}.xlsx') as writer:
            matched_df_checked.to_excel(writer, sheet_name='matched', index=False)
            adjust(matched_df_checked, writer, sheet_name='matched', margin=3, index=False)
            unmatched_df_checked.to_excel(writer, sheet_name='unmatched', index=False)
            adjust(unmatched_df_checked, writer, sheet_name='unmatched', margin=3, index=False)
            excluded_df_checked.to_excel(writer, sheet_name='excluded', index=False)
            adjust(excluded_df_checked, writer, sheet_name='excluded', margin=3, index=False)

        print(f'\nFile created for {client_name} {resource_metric} resource.')

    return
