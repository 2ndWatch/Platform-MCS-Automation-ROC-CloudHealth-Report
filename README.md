
# CHscripts

A brief description of what this project does and who it's for


## ch-getresources.py
Work in progress!

Actions:
- Queries ec2.describe_images and filters out old images
- Queries ec2.describe_snapshots and filters out old snapshots and those created for AMIs
- Queries rds.describe_db_snapshots and filters out old snapshots
- Creates and writes to .csv files for each query

To do:
- add rds.describe_db_cluster_snapshots
- add function for unused AMIs
- add function for unattached EIPs

## ch-parsley.py
Work in progress!

Actions:
- Reads from cypherworxmain-us-east-1-old-images.csv and makes Cypherworx-RAW.xlsx
- Reads from Cypherworx-RAW.xlsx and compares policy-alert-2023-04-28-9345855749691.csv

---- Cypherworx-RAW.xlsx ----

The script will grab info from the AWS generated csv 'cypherworxmain-us-east-1-old-images.csv' and check to see if an AMI was created within the last 90 days. If so, it will copy that entry from the 'main-us-east-1-old-images' sheet to either the 'false-alarms' or 'valid-alarms' sheets.

---- Cypherworx-Matching.xlsx ----

The script verifies if info from Cypherworx-RAW.xlsx sheet 'main-us-east-1-old-images' and info grabbed from CloudHealth 'policy-alert-2023-04-28-9345855749691.csv' match. If they do, they go to the 'matched' sheet, else they go to the 'unmatched' sheet.

## Installation/authentication/usage

Before running any scripts, install the required non-default Python packages: `pip install -r /path/to/requirements.txt`