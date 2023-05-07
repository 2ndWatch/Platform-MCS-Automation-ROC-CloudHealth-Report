import datetime
# import csv


def get_old_rds_snaps(client, account_name, account_number, region_name, cutoff, df_rdssnaps):
    """
    Takes a list of snapshot IDs. Gets all RDS and Aurora cluster snapshots in a region. Writes snapshot properties to
    a .csv if a snapshot is older than the cutoff date and is not in the list of snapshot IDs.
    :param df_rdssnaps:
    :param account_number:
    :param account_name:
    :param client: boto3 client obj
    :param cutoff: str
    :param region_name: str
    :return: count of valid old snapshots
    """
    db_snap_count = 0
    aurora_snap_count = 0

    rds_marker = None
    aurora_marker = None

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
                    print(f'   {db_snap_id} is older than 3 months.')
                    db_snap_count += 1
                    # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Create Date'
                    row = [account_name, account_number, region_name, db_snap_id, db_snap_start]
                    # df.loc[len(df)] = list
                    df_rdssnaps.loc[len(df_rdssnaps)] = row

        try:
            rds_marker = rds_response['Marker']
        except KeyError:
            break

    print(f'   All old RDS snapshots found; getting Aurora cluster snapshots...')

    while True:
        if aurora_marker:
            aurora_response = client.describe_db_cluster_snapshots(Marker=aurora_marker)
        else:
            aurora_response = client.describe_db_cluster_snapshots()

        aurora_snapshots = aurora_response['DBClusterSnapshots']

        for aurora_snap in aurora_snapshots:
            aurora_snap_id = aurora_snap['DBClusterSnapshotIdentifier']
            if 'awsbackup' not in aurora_snap_id:
                aurora_snap_start = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'],
                                                               '%Y-%m-%d %H:%M:%S UTC')
                aurora_snap_date = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'], '%Y-%m-%d')

                if aurora_snap_date < cutoff:
                    print(f'   {aurora_snap_id} is older than 3 months.')
                    aurora_snap_count += 1
                    # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id', 'Create Date'
                    row = [account_name, account_number, region_name, aurora_snap_id, aurora_snap_start]
                    # df.loc[len(df)] = list
                    df_rdssnaps.loc[len(df_rdssnaps)] = row

        try:
            aurora_marker = aurora_response['Marker']
        except KeyError:
            break

    print(f'   All old Aurora cluster snapshots found.')

    # with open(f'{account_name}-{region_name}-rds-snaps.csv', 'w') as csvfile:
    #     fields = ['Snapshot Id', 'Create Date']
    #     writer = csv.writer(csvfile)
    #     writer.writerow(fields)
    #     while True:
    #         if rds_marker:
    #             rds_response = client.describe_db_snapshots(Marker=rds_marker)
    #         else:
    #             rds_response = client.describe_db_snapshots()
    #
    #         db_snapshots = rds_response['DBSnapshots']
    #
    #         for db_snap in db_snapshots:
    #             db_snap_id = db_snap['DBSnapshotIdentifier']
    #
    #             # Ignore any snapshots in 'creating' or 'deleting' state
    #             if db_snap['Status'] == 'available':
    #                 db_snap_start = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d %H:%M:%S UTC')
    #                 db_snap_date = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d')
    #
    #                 if db_snap_date < cutoff:
    #                     print(f'   {db_snap_id} is older than 3 months.')
    #                     db_snap_count += 1
    #                     row = [db_snap_id, db_snap_start]
    #                     writer.writerows([row])
    #
    #         try:
    #             rds_marker = rds_response['Marker']
    #         except KeyError:
    #             break
    #
    #     print(f'   All old RDS snapshots found; getting Aurora cluster snapshots...')
    #
    #     while True:
    #         if aurora_marker:
    #             aurora_response = client.describe_db_cluster_snapshots(Marker=aurora_marker)
    #         else:
    #             aurora_response = client.describe_db_cluster_snapshots()
    #
    #         aurora_snapshots = aurora_response['DBClusterSnapshots']
    #
    #         for aurora_snap in aurora_snapshots:
    #             aurora_snap_id = aurora_snap['DBClusterSnapshotIdentifier']
    #             aurora_snap_start = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'],
    #                                                            '%Y-%m-%d %H:%M:%S UTC')
    #             aurora_snap_date = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'], '%Y-%m-%d')
    #
    #             if aurora_snap_date < cutoff:
    #                 print(f'   {aurora_snap_id} is older than 3 months.')
    #                 aurora_snap_count += 1
    #                 row = [aurora_snap_id, aurora_snap_start]
    #                 writer.writerows([row])
    #
    #         try:
    #             aurora_marker = aurora_response['Marker']
    #         except KeyError:
    #             break
    #
    #     print(f'   All old Aurora cluster snapshots found.')
    #
    # csvfile.close()

    print(f'\n{df_rdssnaps}\n')

    return df_rdssnaps, db_snap_count, aurora_snap_count
