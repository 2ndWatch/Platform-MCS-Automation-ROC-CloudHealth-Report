from modules import create_dataframes as cdf
from UliPlot.XLSX import auto_adjust_xlsx_column_width as adjust
import pandas as pd


def create_file_list(name, date):
    file_list = [
        f'{name} Elastic IPs unattached {date}.xlsx',
        f'{name} EC2 Image older than 3 months {date}.xlsx',
        f'{name} EC2 Snapshots older than 3 months {date}.xlsx',
        f'{name} EBS Volumes unattached {date}.xlsx',
        f'{name} EC2 Image not associated {date}.xlsx',
        f'{name} RDS Snapshots older than 3 months {date}.xlsx'
    ]

    return file_list


def compare_resources(client_name, df_list, file_list, date):
    column_names = ['Public IP', 'Image Id', 'Snapshot Id', 'Volume Id', 'Image Id', 'Snapshot Id']
    metric_list = ['Unassociated-Elastic-IPs', 'Old-AMIs', 'Old-EBS-Snapshots', 'Unattached-Volumes',
                   'Unused-AMIs', 'Old-RDS-Aurora-Snapshots']
    client_df_list = cdf.create_dataframes(for_client=True)

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

        # create new dataframes for matched and unmatched Image Ids
        matched_df = client_df[client_df[column_name].isin(matching_resource_ids)]
        unmatched_df = client_df[~client_df[column_name].isin(matching_resource_ids)]

        # save the dataframes to a new Excel file
        with pd.ExcelWriter(f'{client_name}-{resource_metric}-Matching-{date}.xlsx') as writer:
            matched_df.to_excel(writer, sheet_name='matched', index=False)
            adjust(matched_df, writer, sheet_name='matched', margin=3, index=False)
            unmatched_df.to_excel(writer, sheet_name='unmatched', index=False)
            adjust(unmatched_df, writer, sheet_name='unmatched', margin=3, index=False)

        print(f'\nFile created for {client_name} {resource_metric} resource.')

    return
