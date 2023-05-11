import datetime


def get_old_snapshots(client, account_name, account_number, region_name, snap_list, cutoff, df_ebssnaps):

    snap_count = 0
    valid_count = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_snapshots(OwnerIds=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_snapshots(OwnerIds=[account_number], MaxResults=400)

        snapshots = response['Snapshots']

        for snap in snapshots:
            snap_id = snap['SnapshotId']
            snap_desc = snap['Description']
            snap_size = snap['VolumeSize']
            snap_ami = ''
            snap_start = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d %H:%M:%S UTC')
            snap_date = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d')

            if snap_date < cutoff:
                print(f'   {snap_id} is older than 3 months.')
                snap_count += 1

                if snap_id in snap_list:
                    print(f'      Excluded from results (associated with an old AMI).')
                else:
                    print(f'      Not associated with an AMI on the old AMIs list.')
                    if 'CreateImage' in snap_desc:
                        snap_ami = snap_desc[snap_desc.index('ami'):snap_desc.index('ami') + 21]
                    # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                    # 'Size (GB)', 'Create Date', 'Image Id'
                    row = [account_name, account_number, region_name, snap_id, snap_size, snap_start, snap_ami]
                    df_ebssnaps.loc[len(df_ebssnaps)] = row
                    valid_count += 1

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    # print(f'\n{df_ebssnaps}\n')

    return df_ebssnaps, snap_count, valid_count
