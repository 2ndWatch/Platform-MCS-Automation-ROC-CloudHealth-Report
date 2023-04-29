import datetime
import csv


def get_old_rds_snaps(client, cutoff, profile_name, region_name):
    """
    Takes a list of snapshot IDs. Gets all RDS and Aurora cluster snapshots in a region. Writes snapshot properties to
    a .csv if a snapshot is older than the cutoff date and is not in the list of snapshot IDs.
    :param client: boto3 client obj
    :param cutoff: str
    :param profile_name: str
    :param region_name: str
    :return: count of valid old snapshots
    """
    db_snap_count = 0
    aurora_snap_count = 0
    rds_marker = None
    aurora_marker = None
    with open(f'{profile_name}-{region_name}-rds-snaps.csv', 'w') as csvfile:
        fields = ['Snapshot Id', 'Create Date']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if rds_marker:
                rds_response = client.describe_db_snapshots(Marker=rds_marker)
            else:
                rds_response = client.describe_db_snapshots()

            db_snapshots = rds_response['DBSnapshots']

            for db_snap in db_snapshots:
                db_snap_id = db_snap['DBSnapshotIdentifier']

                # Ignore any snapshots in 'creating' or 'deleting' state
                if db_snap['Status'] == 'available':
                    db_snap_start = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d %H:%M:%S UTC')
                    db_snap_date = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d')

                    if db_snap_date < cutoff:
                        db_snap_count += 1
                        row = [db_snap_id, db_snap_start]
                        writer.writerows([row])

            try:
                rds_marker = rds_response['Marker']
            except KeyError:
                break

        print(f'   RDS snapshots found: {db_snap_count}; getting Aurora cluster snapshots...')

        while True:
            if aurora_marker:
                aurora_response = client.describe_db_cluster_snapshots(Marker=aurora_marker)
            else:
                aurora_response = client.describe_db_cluster_snapshots()

            aurora_snapshots = aurora_response['DBClusterSnapshots']

            for aurora_snap in aurora_snapshots:
                aurora_snap_id = aurora_snap['DBClusterSnapshotIdentifier']
                aurora_snap_start = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'],
                                                               '%Y-%m-%d %H:%M:%S UTC')
                aurora_snap_date = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'], '%Y-%m-%d')

                if aurora_snap_date < cutoff:
                    aurora_snap_count += 1
                    row = [aurora_snap_id, aurora_snap_start]
                    writer.writerows([row])

            try:
                aurora_marker = aurora_response['Marker']
            except KeyError:
                break

        print(f'   Aurora cluster snapshots found: {aurora_snap_count}')

    csvfile.close()

    return db_snap_count + aurora_snap_count
