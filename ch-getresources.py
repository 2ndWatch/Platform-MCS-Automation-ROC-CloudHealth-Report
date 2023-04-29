import boto3
import datetime
import csv

profile_name = "uiwombat"
region_name = "us-east-2"
owner_id = '010949642540'

three_month_cutoff_date = '2023-01-24'

session = boto3.Session(profile_name=profile_name, region_name=region_name)
ec2 = session.client('ec2')
rds = session.client('rds')


def get_old_images():
    """
    Gets all images in a region. Writes image properties to a .csv file if an image is older than the cutoff date and
    was not created by AWS Backup.
    :return: list of all old image IDs; list of valid old image IDs; list of all EBS snapshot IDs associated with old
    images (regardless of whether they were created by AWS Backup)
    """
    global owner_id
    global three_month_cutoff_date
    all_old_images = []
    image_snapshots = []
    valid_old_images = []
    is_next = None
    with open(f'{profile_name}-{region_name}-old-images.csv', 'w') as csvfile:
        fields = ['Image Id', 'Image Name', 'Image Age']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = ec2.describe_images(Owners=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                response = ec2.describe_images(Owners=[owner_id], MaxResults=400)

            images = response['Images']

            for image in images:
                image_id = image['ImageId']  # string
                image_name = image['Name']  # string
                image_storage = image['BlockDeviceMappings']  # list
                image_date = image['CreationDate'][:10]
                image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'

                if image_date < three_month_cutoff_date:
                    all_old_images.append(image_id)
                    if image_storage:
                        image_snapshots = [device['Ebs']['SnapshotId'] for device in image_storage
                                           if 'Ebs' in device.keys()]
                    if 'AwsBackup' not in image_name:
                        valid_old_images.append(image_id)
                        row = [image_id, image_name, image_start]
                        writer.writerows([row])

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return all_old_images, valid_old_images, image_snapshots


# TODO: add function for AMIs not in use older than 3 months
# import list of valid_old_images from previous function


def get_old_snapshots(snap_list):
    """
    Takes a list of snapshot IDs. Gets all snapshots in a region. Writes snapshot properties to a .csv if a snapshot is
    older than the cutoff date and is not in the list of snapshot IDs.
    :param snap_list: list of EBS snapshot IDs
    :return: count of all old snapshots; count of valid old snapshots
    """
    global owner_id
    global three_month_cutoff_date
    snap_count = 0
    valid_count = 0
    is_next = None
    with open(f'{profile_name}-{region_name}-snapshots.csv', 'w') as csvfile:
        fields = ['Snapshot Id', 'Create Date', 'Image Id']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = ec2.describe_snapshots(OwnerIds=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                response = ec2.describe_snapshots(OwnerIds=[owner_id], MaxResults=400)

            snapshots = response['Snapshots']

            for snap in snapshots:
                snap_id = snap['SnapshotId']
                snap_desc = snap['Description']
                snap_ami = ''
                snap_start = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d %H:%M:%S UTC')
                snap_date = datetime.datetime.strftime(snap['StartTime'], '%Y-%m-%d')

                if 'CreateImage' in snap_desc:
                    snap_ami = snap_desc[snap_desc.index('ami'):snap_desc.index('ami') + 21]

                if snap_date < three_month_cutoff_date:
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


# TODO: function for volumes unattached for 4+ weeks (will require CloudTrail API call)
# ec2.describe_volumes


# TODO: add Aurora cluster snapshots
def get_old_rds_snaps():
    """
    Takes a list of snapshot IDs. Gets all RDS and Aurora cluster snapshots in a region. Writes snapshot properties to
    a .csv if a snapshot is older than the cutoff date and is not in the list of snapshot IDs.
    :return: count of valid old snapshots
    """
    global owner_id
    global three_month_cutoff_date
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
                rds_response = rds.describe_db_snapshots(Marker=rds_marker)
            else:
                rds_response = rds.describe_db_snapshots()

            db_snapshots = rds_response['DBSnapshots']

            for db_snap in db_snapshots:
                db_snap_id = db_snap['DBSnapshotIdentifier']
                db_snap_start = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d %H:%M:%S UTC')
                db_snap_date = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d')

                if db_snap_date < three_month_cutoff_date:
                    db_snap_count += 1
                    row = [db_snap_id, db_snap_start]
                    writer.writerows([row])

            try:
                rds_marker = rds_response['Marker']
            except KeyError:
                break

        print(f'RDS snapshots found: {db_snap_count}; getting Aurora cluster snapshots...')

        while True:
            if aurora_marker:
                aurora_response = rds.describe_db_cluster_snapshots(Marker=aurora_marker)
            else:
                aurora_response = rds.describe_db_cluster_snapshots()

            aurora_snapshots = aurora_response['DBClusterSnapshots']

            for aurora_snap in aurora_snapshots:
                aurora_snap_id = aurora_snap['DBClusterSnapshotIdentifier']
                aurora_snap_start = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'],
                                                               '%Y-%m-%d %H:%M:%S UTC')
                aurora_snap_date = datetime.datetime.strftime(aurora_snap['SnapshotCreateTime'], '%Y-%m-%d')

                if aurora_snap_date < three_month_cutoff_date:
                    aurora_snap_count += 1
                    row = [aurora_snap_id, aurora_snap_start]
                    writer.writerows([row])

            try:
                aurora_marker = aurora_response['Marker']
            except KeyError:
                break

        print(f'Aurora cluster snapshots found: {aurora_snap_count}')

    csvfile.close()

    return db_snap_count + aurora_snap_count


# all_old, valid_old, img_snaps = get_old_unused_images()
# print(f'Number of old images for {profile_name} in {region_name}: {len(all_old)}')
# print(f'Number of valid old images for {profile_name} in {region_name}: {len(valid_old)}')

# snapshot_count, valid_snapshot_count = get_old_snapshots(img_snaps)
# print(f'Number of old snapshots for {profile_name} in {region_name}: {snapshot_count}')
# print(f'Number of valid old snapshots for {profile_name} in {region_name}: {valid_snapshot_count}')

db_snapshot_count = get_old_rds_snaps()
print(f'Number of valid old snapshots for {profile_name} in {region_name}: {db_snapshot_count}')
