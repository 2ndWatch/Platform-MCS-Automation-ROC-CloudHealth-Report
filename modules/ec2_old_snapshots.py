import datetime


def get_old_snapshots(client, account_name, account_number, region_name, snap_list, cutoff,
                      df_ebssnaps, df_ebs_cost, logger):
    all_snap_count = 0
    snap_count = 0
    valid_count = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_snapshots(OwnerIds=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_snapshots(OwnerIds=[account_number], MaxResults=400)

        snapshots = response['Snapshots']
        all_snap_count += len(snapshots)
        logger.info(f'Snapshots found: {all_snap_count}')

        for snap in snapshots:
            snap_id = snap['SnapshotId']
            snap_desc = snap['Description']
            snap_size = snap['VolumeSize']
            snap_ami = ''
            snap_start = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d %H:%M:%S UTC')
            snap_date = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d')
            storage_cost = 0

            if snap_date < cutoff:
                logger.debug(f'   {snap_id} is older than 3 months.')
                snap_count += 1

                if snap_id in snap_list:
                    logger.debug(f'      Excluded from results (associated with an old AMI).')
                else:
                    logger.debug(f'      Not associated with an AMI on the old AMIs list.')
                    if 'CreateImage' in snap_desc:
                        snap_ami = snap_desc[snap_desc.index('ami'):snap_desc.index('ami') + 21]
                    try:
                        cost = df_ebs_cost.loc[df_ebs_cost['ResourceId'] == snap_id,
                                               'Cost'].values[0].item()
                        storage_cost += cost
                    except IndexError:
                        continue
                    # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                    # 'Size (GB)', 'Create Date', 'Image Id', 'Cost Per Month'
                    row = [account_name, account_number, region_name, snap_id, snap_size,
                           snap_start, snap_ami, round(storage_cost, 2)]
                    df_ebssnaps.loc[len(df_ebssnaps)] = row
                    valid_count += 1

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    return df_ebssnaps, snap_count, valid_count
