import datetime


def get_old_rds_snaps(client, account_name, account_number, region_name, cutoff, df_rdssnaps, logger):
    all_snaps_count = 0
    db_snap_count = 0
    aurora_snap_count = 0

    # Marker for responses over the max length; tells AWS where the last API call left off
    rds_marker = None
    aurora_marker = None

    while True:
        if rds_marker:
            rds_response = client.describe_db_snapshots(Marker=rds_marker)
        else:
            rds_response = client.describe_db_snapshots()

        db_snapshots = rds_response['DBSnapshots']

        all_snaps_count += len(db_snapshots)
        logger.info(f'RDS snapshots found: {all_snaps_count}')

        for db_snap in db_snapshots:
            db_snap_id = db_snap['DBSnapshotIdentifier']
            db_snap_size = db_snap['AllocatedStorage']
            db_instance_id = db_snap['DBInstanceIdentifier']

            # Ignore any snapshots in 'creating' or 'deleting' state
            if db_snap['Status'] == 'available':
                db_snap_start = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d %H:%M:%S UTC')
                db_snap_date = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d')

                # Filter for snapshots older than 3 months
                if db_snap_date < cutoff:
                    logger.debug(f'   {db_snap_id} is older than 3 months.')
                    db_snap_count += 1

                    # Dataframe column names:
                    # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                    # 'Instance Id', 'Size (GB)', 'Create Date'
                    row = [account_name, account_number, region_name, db_snap_id,
                           db_instance_id, db_snap_size, db_snap_start]
                    df_rdssnaps.loc[len(df_rdssnaps)] = row

        try:
            rds_marker = rds_response['Marker']
        except KeyError:
            break

    logger.debug(f'   All old RDS snapshots found; getting Aurora cluster snapshots...')

    while True:
        if aurora_marker:
            aurora_response = client.describe_db_cluster_snapshots(Marker=aurora_marker)
        else:
            aurora_response = client.describe_db_cluster_snapshots()

        aurora_snapshots = aurora_response['DBClusterSnapshots']

        all_snaps_count += len(aurora_snapshots)
        logger.info(f'Aurora snapshots found: {all_snaps_count}')

        for aurora_snap in aurora_snapshots:
            aurora_snap_id = aurora_snap['DBClusterSnapshotIdentifier']
            aurora_snap_size = aurora_snap['AllocatedStorage']
            aurora_cluster_id = aurora_snap['DBClusterIdentifier']

            aurora_snap_start = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'],
                                                           '%Y-%m-%d %H:%M:%S UTC')
            aurora_snap_date = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'], '%Y-%m-%d')

            # Filter for snapshots older than 3 months
            if aurora_snap_date < cutoff:
                logger.debug(f'   {aurora_snap_id} is older than 3 months.')
                aurora_snap_count += 1

                # Dataframe column names:
                # 'Account Name', 'Account Number', 'Region Name', 'Snapshot Id',
                # 'Instance Id', 'Size (GB)', 'Create Date'
                row = [account_name, account_number, region_name, aurora_snap_id,
                       aurora_cluster_id, aurora_snap_size, aurora_snap_start]
                df_rdssnaps.loc[len(df_rdssnaps)] = row

        try:
            aurora_marker = aurora_response['Marker']
        except KeyError:
            break

    logger.debug(f'   All old Aurora cluster snapshots found.')

    return df_rdssnaps, db_snap_count, aurora_snap_count
