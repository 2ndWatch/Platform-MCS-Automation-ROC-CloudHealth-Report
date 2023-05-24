from datetime import datetime, timedelta
import time
import tqdm
import json

with open('src/vol_cost.txt') as vc:
    vc_txt = vc.read()
vol_cost_dict = json.loads(vc_txt)


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
                               region_name, report_date, df_vol, logger):

    unatt_count = 0
    valid_count = 0

    is_next = None

    while True:
        if is_next:
            response = ec2_client.describe_volumes(MaxResults=400, NextToken=is_next)
        else:
            response = ec2_client.describe_volumes(MaxResults=400)

        volumes = response['Volumes']

        unatt_vols = []
        for volume in volumes:
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
            four_week_delta_date = (datetime.strptime(report_date, '%Y-%m-%d') - timedelta(weeks=4)).date()
            for volume in unatt_vols:
                volume_name = volume['name']
                volume_size = volume['size']
                volume_type = volume['type']
                volume_iops = volume['iops']
                volume_throughput = volume['throughput']
                logger.debug(f'   Unattached volume found: {volume_name}. CloudTrail request sent.')
                logger.info(f'   Unattached volume found. CloudTrail request sent.')
                unatt_count += 1

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

                    # 'Account Name', 'Account Number', 'Region Name', 'Volume Id', 'Size (GB)',
                    # 'Volume Type', 'Cost Per Month'
                    row = [account_name, account_number, region_name, volume_name, volume_size,
                           volume_type, volume_cost]
                    df_vol.loc[len(df_vol)] = row
                    valid_count += 1

                if unatt_count < len(unatt_vols):
                    logger.info('      Waiting 31 seconds to avoid CloudTrail API request throttling...')
                    for _ in tqdm.tqdm(range(31)):
                        time.sleep(1)

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    df_vol.style.format({
        'Cost Per Month': "{:.2f}"
    })

    return df_vol, unatt_count, valid_count
