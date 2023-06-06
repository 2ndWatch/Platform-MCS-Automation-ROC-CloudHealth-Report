import modules.get_cloudhealth_resources as gcr
import modules.create_dataframes as cdf
import pandas as pd
import json

# Read the clients.txt file into a dictionary
# TODO: change file path to 'src/clients.txt'
with open('../src/clients.txt') as cl:
    cl_txt = cl.read()
clients_dict = json.loads(cl_txt)

# Client keys selected by user
client_keys = ['b']
client_ch_name = clients_dict['b']['name']

ch_policy_violations, alerts_dict = gcr.get_cloudhealth_resources(client_ch_name)

alert_keys = []
for key in alerts_dict.keys():
    alert_keys.append(key)
print(alert_keys)

print(ch_policy_violations)

# Create 6 empty dataframes for the Cloud health data
df_ch_eips, df_ch_oldimages, df_ch_ebssnaps, df_ch_vol, df_ch_unami, df_ch_rdssnaps, \
    columns_ch_list, empty_excluded_ch_row = cdf.create_cloudhealth_dataframes()

# TODO: Fill Cloud Health dataframes via API calls; this only happens once per client

ch_df_list = [df_ch_eips, df_ch_oldimages, df_ch_ebssnaps, df_ch_vol, df_ch_unami, df_ch_rdssnaps]

working_ch_resources = ch_policy_violations[0]
affected_resources = working_ch_resources[alert_keys[0]]['affected_resources']
eip_dataframe = ch_df_list[0]

print(affected_resources[0])

for j in range(len(affected_resources)):
    eip_dataframe = pd.concat([eip_dataframe, pd.DataFrame(affected_resources[j], index=[j])])

pd.set_option('display.max_columns', None)
print(eip_dataframe.head(3))
# TODO: drop column names? Asset ID, AWS Account ID


print(ch_df_list[0].head(3))
