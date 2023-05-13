from modules import create_dataframes as cdf
from UliPlot.XLSX import auto_adjust_xlsx_column_width as adjust
import pandas as pd


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


def fill_empty_df(validated_df, excluded_df, empty_unmatched_row, empty_excluded_row, columns_list, i):
    if validated_df.empty:
        print('   Empty dataframe, adding "No resources matched" entry.')
        validated_df.loc[1] = empty_unmatched_row[i]
    if excluded_df.empty:
        try:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            # print(excluded_df)
            # print(empty_excluded_row[i])
            excluded_df = pd.concat([excluded_df, pd.DataFrame([empty_excluded_row[i]], columns=columns_list[i])],
                                    ignore_index=True)
        except ValueError:
            print('   Empty dataframe, adding "No resources excluded" entry.')
            excluded_df = pd.concat([excluded_df, pd.DataFrame([empty_unmatched_row[i]], columns=columns_list[i])],
                                    ignore_index=True)
    return validated_df, excluded_df


def compare_resources(client_name, df_list, file_list, date):
    column_names = ['Public IP', 'Image Id', 'Snapshot Id', 'Volume Id', 'Image Id', 'Snapshot Id']
    metric_list = ['Unassociated Elastic IPs', 'Old AMIs', 'Old EBS Snapshots', 'Unattached Volumes',
                   'Unused AMIs', 'Old RDS Snapshots']
    client_df_list, columns_list, empty_unmatched_row, empty_excluded_row = cdf.create_dataframes(for_client=True)

    for i in range(6):
        client_df = df_list[i]
        # print(f'client df types:\n{client_df.dtypes}')
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
        # matched, unmatched, & validated might be unnecessary
        matched_df = client_df[client_df[column_name].isin(matching_resource_ids)]
        unmatched_df = client_df[~client_df[column_name].isin(matching_resource_ids)]
        validated_df = pd.concat([matched_df, unmatched_df])
        excluded_df = cloudhealth_df[~cloudhealth_df[column_name].isin(matching_resource_ids)]

        # Add a 'No resources' row to any empty dataframes
        # new_df_list = [matched_df, unmatched_df]
        validated_df_checked, excluded_df_checked = fill_empty_df(validated_df, excluded_df, empty_unmatched_row,
                                                                  empty_excluded_row, columns_list, i)

        # save the dataframes to Excel files
        # TODO: should be a better way to check if the file exists and create it if it doesn't before adding sheets
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
                excluded_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(excluded_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(f'output/{client_name}-Excluded-{date}.xlsx') as writer:
                excluded_df_checked.to_excel(writer, sheet_name=f'{metric_list[i]}', index=False)
                adjust(excluded_df_checked, writer, sheet_name=f'{metric_list[i]}', margin=3, index=False)

        print(f'\nTab created for {client_name} {resource_metric}.')

    return
