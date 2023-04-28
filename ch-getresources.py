import boto3
import datetime
import csv

profile_name = "cypherworxmain"
region_name = "us-east-1"
owner_id = '372356060901'

three_month_cutoff_date = '2023-01-24'

session = boto3.Session(profile_name=profile_name, region_name=region_name)
ec2 = session.client('ec2')
rds = session.client('rds')


def get_old_images():
    global owner_id
    global three_month_cutoff_date
    all_old_images = []
    image_snapshots = []
    valid_old_images = []
    is_next = None
    with open(f'{profile_name}-{region_name}-old-images.csv', 'w') as csvfile:
        # TODO: add Image Name
        fields = ['Image Id', 'Image Age']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                # response = ec2.describe_images(Owners=[owner_id], ImageIds=['ami-0dcee45efbc07e5ce'])
                response = ec2.describe_images(Owners=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                # response = ec2.describe_images(Owners=[owner_id], ImageIds=['ami-0dcee45efbc07e5ce'])
                response = ec2.describe_images(Owners=[owner_id], MaxResults=400)

            images = response['Images']
            # print(f"Response contains {len(images)} images.")

            for image in images:
                image_id = image['ImageId']  # string
                image_name = image['Name']  # string
                image_storage = image['BlockDeviceMappings']  # list
                image_date = image['CreationDate'][:10]
                image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'

                if image_date < three_month_cutoff_date:
                    all_old_images.append(image_id)
                    # assuming we filter out snaps from old aws backups; else, move this loop into the next `if` block
                    if image_storage:
                        for device in image_storage:
                            if 'Ebs' in device.keys():
                                image_snapshots.append(device['Ebs']['SnapshotId'])
                    if 'AwsBackup' not in image_name:
                        valid_old_images.append(image_id)
                        row = [image_id, image_start]
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
            # print(f"Response contains {len(snapshots)} snapshots.")

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
# describe_db_cluster_snapshots
def get_old_rds_snaps():
    global owner_id
    global three_month_cutoff_date
    db_snap_count = 0
    marker = None
    with open(f'{profile_name}-{region_name}-rds-snaps.csv', 'w') as csvfile:
        fields = ['Snapshot Id', 'Create Date']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if marker:
                response = rds.describe_db_snapshots(Marker=marker)
            else:
                # response = rds.describe_db_snapshots(DBSnapshotIdentifier='argentina-setup-2-final-snapshot')
                response = rds.describe_db_snapshots()

            db_snapshots = response['DBSnapshots']
            # print(f"Response contains {len(db_snapshots)} snapshots.")

            for db_snap in db_snapshots:
                db_snap_id = db_snap['DBSnapshotIdentifier']
                # print(db_snap_id)
                db_snap_start = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d %H:%M:%S UTC')
                db_snap_date = datetime.datetime.strftime(db_snap['SnapshotCreateTime'], '%Y-%m-%d')
                # print(db_snap_date)

                if db_snap_date < three_month_cutoff_date:
                    # print('Old snapshot!')
                    db_snap_count += 1
                    row = [db_snap_id, db_snap_start]
                    writer.writerows([row])

            try:
                marker = response['Marker']
            except KeyError:
                break

    csvfile.close()

    return db_snap_count


# all_old, valid_old, img_snaps = get_old_unused_images()
# print(f'Number of old images for {profile_name} in {region_name}: {len(all_old)}')
# print(f'Number of valid old images for {profile_name} in {region_name}: {len(valid_old)}')

# snapshot_count, valid_snapshot_count = get_old_snapshots(img_snaps)
# print(f'Number of old snapshots for {profile_name} in {region_name}: {snapshot_count}')
# print(f'Number of valid old snapshots for {profile_name} in {region_name}: {valid_snapshot_count}')

db_snapshot_count = get_old_rds_snaps()
print(f'Number of valid old snapshots for {profile_name} in {region_name}: {db_snapshot_count}')
