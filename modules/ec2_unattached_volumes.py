from datetime import datetime, timedelta
import time
import tqdm
import json

# Read the vol_cost.json file into a dictionary
with open('src/vol_cost.json') as vc:
    vc_txt = vc.read()
vol_cost_dict = json.loads(vc_txt)


# Calculate the cost of a volume based on its type, size, properties, and region
def calculate_storage_price(region_name, volume_size, volume_type, volume_iops, volume_throughput):
    cost = 0
    region_cost_dict = vol_cost_dict[region_name]
    cost_dict = region_cost_dict[volume_type]

    cost += volume_size * cost_dict['storage']

    if volume_type == 'gp3':
        if volume_iops > 3000:
            cost += (volume_iops - 3000) * cost_dict['iops_over_3k']
        if volume_throughput > 125:
            cost += (volume_throughput - 125) * cost_dict['through_over_125']
    if volume_type == 'io1':
        cost += volume_iops * cost_dict['iops']
    if volume_type == 'io2':
        if volume_iops > 32000:
            cost += ((volume_iops - 32000) * cost_dict['iops_over_32k']) + (32000 * cost_dict['iops_under_32k'])
        else:
            cost += volume_iops * cost_dict['iops_under_32k']

    return cost


def get_old_unattached_volumes(ec2_client, cloudtrail_client, account_name, account_number,
                               region_name, today, df_vol, logger):
    all_vols_count = 0
    unatt_count = 0
    valid_count = 0

    is_next = None

    while True:
        if is_next:
            response = ec2_client.describe_volumes(MaxResults=400, NextToken=is_next)
        else:
            response = ec2_client.describe_volumes(MaxResults=400)

        volumes = response['Volumes']

        all_vols_count += len(volumes)
        logger.info(f'Volumes found: {all_vols_count}')

        unatt_vols = []
        for volume in volumes:

            # Filter for volumes that are not attached and add to the unatt_vols list
            if not volume['Attachments']:
                vol_dict = {'name': volume['VolumeId'], 'size': volume['Size'], 'type': volume['VolumeType']}
                try:
                    vol_dict['iops'] = volume['Iops']
                except KeyError:
                    vol_dict['iops'] = ''
                try:
                    vol_dict['throughput'] = volume['Throughput']
                except KeyError:
                    vol_dict['throughput'] = ''
                unatt_vols.append(vol_dict)

        if unatt_vols:
            four_week_delta_date = (datetime.strptime(today, '%Y-%m-%d') - timedelta(weeks=4)).date()
            for volume in unatt_vols:
                volume_name = volume['name']
                volume_size = volume['size']
                volume_type = volume['type']
                volume_iops = volume['iops']
                volume_throughput = volume['throughput']
                logger.debug(f'   Unattached volume found: {volume_name}. CloudTrail request sent.')
                logger.info(f'   Unattached volume found. CloudTrail request sent.')
                unatt_count += 1

                # For any unattached volume, make a call to CloudTrail to check if it was unattached within the
                # past four weeks
                ct_response = cloudtrail_client.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName',
                                                                                 'AttributeValue': f'{volume}'}])

                events = ct_response['Events']
                logger.debug(f'      There are {len(events)} event(s) for this volume.')

                unatt_four_weeks = True
                if events:
                    for event in events:
                        if event['EventName'] == 'DetachVolume':
                            event_date = event['EventTime'].date()
                            if event_date > four_week_delta_date:
                                unatt_four_weeks = False
                                print(f'      {volume} has NOT been unattached for four weeks.')

                if unatt_four_weeks:
                    logger.debug(f'      {volume} has been unattached for more than four weeks.')

                    # Calculate cost per month
                    volume_cost = calculate_storage_price(region_name, volume_size, volume_type,
                                                          volume_iops, volume_throughput)

                    # Dataframe column names:
                    # 'Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)',
                    # 'Volume Type', 'Cost Per Month'
                    row = [account_name, account_number, region_name, volume_name, volume_size,
                           volume_type, volume_cost]
                    df_vol.loc[len(df_vol)] = row
                    valid_count += 1

                # If there are more unattached volumes to check, pause for 31 seconds to avoid CloudTrail API
                # throttling (max 2 requests per minute)
                if unatt_count < len(unatt_vols):
                    logger.info('      Waiting 31 seconds to avoid CloudTrail API request throttling...')

                    # Create a progress bar in the console to track each pause
                    for _ in tqdm.tqdm(range(31)):
                        time.sleep(1)

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    return df_vol, unatt_count, valid_count
