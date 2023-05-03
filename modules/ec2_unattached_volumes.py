import csv
from datetime import datetime, timedelta
import time


def get_old_unattached_volumes(ec2_client, cloudtrail_client, report_date, profile_name, region_name):
    """

    :return:
    """
    unatt_count = 0
    valid_count = 0
    is_next = None
    with open(f'{profile_name}-{region_name}-unatt-volumes.csv', 'w') as csvfile:
        fields = ['Volume Id']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = ec2_client.describe_volumes(MaxResults=400, NextToken=is_next)
            else:
                response = ec2_client.describe_volumes(MaxResults=400)

            volumes = response['Volumes']

            unatt_vols = [volume['VolumeId'] for volume in volumes if not volume['Attachments']]

            if unatt_vols:
                four_week_delta_date = (datetime.strptime(report_date, '%Y-%m-%d') - timedelta(weeks=4)).date()
                for volume in unatt_vols:
                    print(f'   Unattached volume found: {volume}')
                    unatt_count += 1

                    ct_response = cloudtrail_client.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName',
                                                                                     'AttributeValue': f'{volume}'}])

                    events = ct_response['Events']
                    print(f'      There are {len(events)} event(s) for this volume.')

                    unatt_four_weeks = True
                    if events:
                        for event in events:
                            if event['EventName'] == 'DetachVolume':
                                event_date = event['EventTime'].date()
                                if event_date > four_week_delta_date:
                                    unatt_four_weeks = False
                                    print(f'      {volume} has NOT been unattached for four weeks.')

                    if unatt_four_weeks:
                        print(f'      {volume} has been unattached for more than four weeks.')
                        row = [volume]
                        writer.writerows([row])
                        valid_count += 1

                    if unatt_count < len(unatt_vols):
                        print('         Waiting 31 seconds to avoid CloudTrail API request throttling...')
                        time.sleep(31)

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return unatt_count, valid_count
