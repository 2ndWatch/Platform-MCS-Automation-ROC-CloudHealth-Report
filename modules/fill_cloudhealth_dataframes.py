import modules.get_cloudhealth_resources as gcr
import modules.create_dataframes as cdf
import pandas as pd


def fill_cloudhealth_dataframes(client_name, logger):
    ch_policy_violations, alerts_dict = gcr.get_cloudhealth_resources(client_name, logger)

    alert_keys = []
    for key in alerts_dict.keys():
        alert_keys.append(key)

    # Create 6 empty dataframes for the Cloud health data and put them into a list
    ch_df_list = cdf.create_cloudhealth_dataframes()

    filled_dataframes = []

    # Fill Cloud Health dataframes via API calls and add to a list
    for i in range(len(ch_policy_violations)):
        working_ch_resources = ch_policy_violations[i]
        affected_resources = working_ch_resources[alert_keys[i]]['affected_resources']
        dataframe_to_fill = ch_df_list[i]

        if affected_resources:
            for j in range(len(affected_resources)):
                dataframe_to_fill = pd.concat([dataframe_to_fill, pd.DataFrame(affected_resources[j], index=[j])])

            dataframe_to_fill = dataframe_to_fill.drop(columns=['Asset ID', 'AWS Account ID'])
        filled_dataframes.append(dataframe_to_fill)

    return filled_dataframes
