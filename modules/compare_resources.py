from modules import create_dataframes as cdf
from UliPlot.XLSX import auto_adjust_xlsx_column_width as adjust
import pandas as pd


def create_file_list(name, date):
    file_list_csv = [
        f'{name} eip unattached {date}.csv',
        f'{name} ec2 image 3 months {date}.csv',
        f'{name} ec2 snaps 3 months {date}.csv',
        f'{name} ebs unattached {date}.csv',
        f'{name} ec2 image unused {date}.csv',
        f'{name} rds snaps 3 months {date}.csv'
    ]

    return file_list_csv


def fill_empty_df(validated_df, excluded_csv_df, empty_unmatched_row, empty_excluded_row, columns_list, i):
    if validated_df.empty:
        print('   Empty dataframe, adding "No resources matched" entry.')
        validated_df.loc[1] = empty_unmatched_row[i]
    if excluded_csv_df.empty:
        try:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            excluded_csv_df = pd.concat([excluded_csv_df, pd.DataFrame([empty_excluded_row[i]],
                                                                       columns=columns_list[i])],
                                        ignore_index=True)
        except ValueError:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            excluded_csv_df = pd.concat([excluded_csv_df, pd.DataFrame([empty_unmatched_row[i]],
                                                                       columns=columns_list[i])],
                                        ignore_index=True)
    return validated_df, excluded_csv_df


def compare_resources(client_name, df_list, file_list_csv, date):
    column_names = ['Public IP', 'Image Id', 'Snapshot Id', 'Volume Id', 'Image Id', 'Snapshot Id']
    metric_list = ['Unassociated Elastic IPs', 'Old AMIs', 'Old EBS Snapshots', 'Unattached Volumes',
                   'Unused AMIs', 'Old RDS Snapshots']
    client_df_list, columns_list, empty_unmatched_row, empty_excluded_row = cdf.create_dataframes(for_client=True)

    for i in range(6):
        client_df = df_list[i]
        csv_file = file_list_csv[i]
        column_name = column_names[i]
        resource_metric = metric_list[i]

        try:
            cloudhealth_csv_df = pd.read_csv(f'cloudhealth/{csv_file}')
        except FileNotFoundError:
            print('File not found, creating placeholder dataframe instead...')
            cloudhealth_csv_df = client_df_list[i]

        client_resource_ids = set(client_df[column_name])
        cloudhealth_csv_resource_ids = set(cloudhealth_csv_df[column_name])

        # find the intersection of the two sets of resource ids (i.e. the matching ones)
        matching_resource_ids = cloudhealth_csv_resource_ids.intersection(client_resource_ids)

        # create new dataframes for matched, unmatched, and excluded resource ids
        matched_df = client_df[client_df[column_name].isin(matching_resource_ids)]
        unmatched_df = client_df[~client_df[column_name].isin(matching_resource_ids)]
        validated_df = pd.concat([matched_df, unmatched_df])
        excluded_csv_df = cloudhealth_csv_df[~cloudhealth_csv_df[column_name].isin(matching_resource_ids)]

        # Add a 'No resources' row to any empty dataframes
        validated_df_checked, excluded_csv_df_checked = fill_empty_df(validated_df, excluded_csv_df,
                                                                      empty_unmatched_row, empty_excluded_row,
                                                                      columns_list, i)

        # save the dataframes to Excel files
        # TODO: should be a better way to check if the file exists and create it if it doesn't before adding sheets
        #  because this looks pretty awful. maybe make this a function and pass variables in?
        try:
            with pd.ExcelWriter(f'output/{client_name}-Validated-{date}.xlsx', mode='a', if_sheet_exists='replace') \
                    as writer:
                validated_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(validated_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(f'output/{client_name}-Validated-{date}.xlsx') as writer:
                validated_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(validated_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)
        try:
            with pd.ExcelWriter(f'output/{client_name}-Excluded-{date}.xlsx', mode='a', if_sheet_exists='replace') \
                    as writer:
                excluded_csv_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(excluded_csv_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(f'output/{client_name}-Excluded-{date}.xlsx') as writer:
                excluded_csv_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(excluded_csv_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)

        print(f'\nTab created for {client_name} {resource_metric}.')

    return
