import csv
import datetime


def get_old_snapshots(client, snap_list, owner_id, cutoff, profile_name, region_name):
    """
    Takes a list of snapshot IDs. Gets all snapshots in a region. Writes snapshot properties to a .csv if a snapshot is
    older than the cutoff date and is not in the list of snapshot IDs.
    :param client: boto3 client obj
    :param snap_list: list
    :param owner_id: str
    :param cutoff: str
    :param profile_name: str
    :param region_name: str
    :return: count of all old snapshots; count of valid old snapshots
    """
    snap_count = 0
    valid_count = 0
    is_next = None
    with open(f'{profile_name}-{region_name}-snapshots.csv', 'w') as csvfile:
        fields = ['Snapshot Id', 'Create Date', 'Image Id']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = client.describe_snapshots(OwnerIds=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                response = client.describe_snapshots(OwnerIds=[owner_id], MaxResults=400)

            snapshots = response['Snapshots']

            for snap in snapshots:
                snap_id = snap['SnapshotId']
                snap_desc = snap['Description']
                snap_ami = ''
                snap_start = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d %H:%M:%S UTC')
                snap_date = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d')

                if 'CreateImage' in snap_desc:
                    snap_ami = snap_desc[snap_desc.index('ami'):snap_desc.index('ami') + 21]

                if snap_date < cutoff:
                    snap_count += 1

                    """
                    Filter out any snapshots created for an existing AMI; if an AMI no longer exists, the 
                    corresponding snapshot will be added to the report
                    """
                    if snap_id not in snap_list:
                        row = [snap_id, snap_start, snap_ami]
                        writer.writerows([row])
                        valid_count += 1

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return snap_count, valid_count
