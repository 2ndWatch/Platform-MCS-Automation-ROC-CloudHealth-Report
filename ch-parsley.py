import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil import parser

# -----Begin unneeded code

# read the original CSV file and write to Excel
csvDataframe = pd.read_csv('cypherworxmain-us-east-1-old-images.csv')
resultExcelFile = pd.ExcelWriter("Cypherworx-RAW.xlsx")
csvDataframe.to_excel(resultExcelFile, sheet_name="main-us-east-1-old-images", index=False)
resultExcelFile.close()

# read from the Excel file
xlsx = pd.ExcelFile("Cypherworx-RAW.xlsx")
df = pd.read_excel(xlsx, "main-us-east-1-old-images")

# Create a new dataframe for the rows that satisfy the condition
false_alarms_df = pd.DataFrame(columns=df.columns)
valid_alarms_df = pd.DataFrame(columns=df.columns)

# Loop through each row in the original dataframe
for index, row in df.iterrows():
    # Get the date value in column B for the current row
    date_str = row['Image Age']
    date_obj = parser.parse(date_str)

    # Check if the date is not older than 3 months
    if date_obj >= datetime.now(timezone.utc) - timedelta(days=90):
        # Add the row to the valid_alarms_df if it's a valid alarm
        if 'Alarm Status' in row.index and row['Alarm Status'] == 'Valid':
            valid_alarms_df = pd.concat([valid_alarms_df, row.to_frame().transpose()], ignore_index=True)
        # Add the row to the false_alarms_df if it's an invalid alarm
        else:
            false_alarms_df = pd.concat([false_alarms_df, row.to_frame().transpose()], ignore_index=True)
    else:
        valid_alarms_df = pd.concat([valid_alarms_df, row.to_frame().transpose()], ignore_index=True)

# Save the new dataframes to other sheets
with pd.ExcelWriter('Cypherworx-RAW.xlsx', mode='a') as writer:
    false_alarms_df.to_excel(writer, sheet_name="false-alarms", index=False)
    valid_alarms_df.to_excel(writer, sheet_name="valid-alarms", index=False)

# -----End

# read in the CloudHealth report and extract the Image Id column
cloudhealth_df = pd.read_csv("policy-alert-2023-04-28-9345855749691.csv")
cloudhealth_image_ids = set(cloudhealth_df["Image Id"])

# read in the Cypherworx-RAW.xlsx file and extract the Image Id column
cypherworx_df = pd.read_excel("Cypherworx-RAW.xlsx", sheet_name="main-us-east-1-old-images")
cypherworx_image_ids = set(cypherworx_df["Image Id"])

# find the intersection of the two sets of Image Ids (i.e. the matching ones)
matching_image_ids = cloudhealth_image_ids.intersection(cypherworx_image_ids)

# create new dataframes for matched and unmatched Image Ids
matched_df = cypherworx_df[cypherworx_df["Image Id"].isin(matching_image_ids)]
unmatched_df = cypherworx_df[~cypherworx_df["Image Id"].isin(matching_image_ids)]

# save the dataframes to a new Excel file
with pd.ExcelWriter('Cypherworx-Matching.xlsx') as writer:
    matched_df.to_excel(writer, sheet_name="matched", index=False)
    unmatched_df.to_excel(writer, sheet_name="unmatched", index=False)
