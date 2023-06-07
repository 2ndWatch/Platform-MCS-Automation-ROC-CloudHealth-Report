from modules import create_dataframes as cdf
from UliPlot.XLSX import auto_adjust_xlsx_column_width as adjust
import pandas as pd


# Add a 'No resources matched' or 'No resources excluded' line to any empty dataframes
def fill_empty_df(validated_df, excluded_df, empty_unmatched_row, empty_excluded_row, columns_list, i, logger):
    if validated_df.empty:
        logger.debug('\nEmpty dataframe, adding "No resources matched" entry.')
        validated_df.loc[1] = empty_unmatched_row[i]
    if excluded_df.empty:
        try:
            logger.debug('\nEmpty dataframe, adding "No resources excluded" entry.')
            excluded_df = pd.concat([excluded_df, pd.DataFrame([empty_excluded_row[i]],
                                                               columns=columns_list[i])],
                                    ignore_index=True)
        except ValueError:
            logger.debug('\nEmpty dataframe, adding "No resources excluded" entry.')
            excluded_df = pd.concat([excluded_df, pd.DataFrame([empty_unmatched_row[i]],
                                                               columns=columns_list[i])],
                                    ignore_index=True)
    return validated_df, excluded_df


# Compare resources between this program and Cloud Health
def compare_resources(client_name, filled_client_dataframes, filled_ch_dataframes, date, logger):
    column_names = ['Public IP', 'Image Id', 'Snapshot Id', 'Volume Id', 'Image Id', 'Snapshot Id']
    metric_list = ['Unassociated Elastic IPs', 'Old AMIs', 'Old EBS Snapshots', 'Unattached Volumes',
                   'Unused AMIs', 'Old RDS Snapshots']

    # Create column and row lists
    # client_df_list, columns_list, empty_unmatched_row, empty_excluded_row = cdf.create_dataframes(for_client=True)
    columns_list, empty_unmatched_row, columns_ch_list, empty_excluded_row = cdf.create_column_lists_empty_rows()

    for i in range(6):
        client_dataframe = filled_client_dataframes[i]
        ch_dataframe = filled_ch_dataframes[i]
        column_name = column_names[i]
        resource_metric = metric_list[i]

        client_resource_ids = set(client_dataframe[column_name])
        cloudhealth_csv_resource_ids = set(ch_dataframe[column_name])

        # find the intersection of the two sets of resource ids (i.e. the matching ones)
        matching_resource_ids = cloudhealth_csv_resource_ids.intersection(client_resource_ids)

        # create new dataframes for matched, unmatched, and excluded resource ids
        matched_df = client_dataframe[client_dataframe[column_name].isin(matching_resource_ids)]
        unmatched_df = client_dataframe[~client_dataframe[column_name].isin(matching_resource_ids)]
        validated_df = pd.concat([matched_df, unmatched_df])
        excluded_df = ch_dataframe[~ch_dataframe[column_name].isin(matching_resource_ids)]

        # Add a 'No resources' row to any empty dataframes
        validated_df_checked, excluded_df_checked = fill_empty_df(validated_df, excluded_df, empty_unmatched_row,
                                                                  empty_excluded_row, columns_list, i, logger)

        # save the dataframes to Excel files
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

        logger.debug(f'\nTab created for {client_name} {resource_metric}.')

    return
