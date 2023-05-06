import boto3
from modules import ec2_old_images as eold
from modules import ec2_old_snapshots as esnap
from modules import rds_old_snapshots as rsnap
from modules import ec2_unused_amis as euna
from modules import ec2_unattached_volumes as euvo
from modules import ec2_elastic_ips as eips


def get_resources(profile, region, report_date, three_month_cutoff_date,
                  df_eips, df_oldami, df_ebssnaps, df_vol, df_unami, df_rdssnaps):
    profile_name = profile['profile_name']
    region_name = region
    account_number = profile['account_number']

    session = boto3.Session(region_name=region_name)
    ec2 = session.client('ec2')
    rds = session.client('rds')
    ct = session.client('cloudtrail')

    print(f'Starting Cloud Health validation for {profile_name} in {region_name}.\n')
    print('Getting EC2 images older than 3 months...')
    valid_old, img_snaps = eold.get_old_images(ec2, account_number, three_month_cutoff_date, profile_name, region_name)
    print(f'   Number of valid old images: {len(valid_old)}')
    print(f'   Number of AMI-associated snapshots: {len(img_snaps)}')

    print('Getting EBS snapshots older than 3 months...')
    snapshot_count, valid_snapshot_count = esnap.get_old_snapshots(ec2, img_snaps, account_number,
                                                                   three_month_cutoff_date, profile_name, region_name)
    print(f'   Number of old EBS snapshots: {snapshot_count}')
    print(f'   Number of valid old EBS snapshots: {valid_snapshot_count}')

    print('Getting RDS and Aurora snapshots older than 3 months...')
    db_snapshot_count, aurora_snapshot_count = rsnap.get_old_rds_snaps(rds, three_month_cutoff_date,
                                                                       profile_name, region_name)
    print(f'   Number of valid old RDS snapshots: {db_snapshot_count}')
    print(f'   Number of valid old Aurora snapshots: {aurora_snapshot_count}')

    print('Getting unused EC2 images...')
    unused_image_count = euna.get_unused_images(ec2, account_number, valid_old, profile_name, region_name)
    print(f'   Number of valid unused images: {unused_image_count}')

    print('Getting unattached EC2 volumes...')
    unatt_volume_count, valid_volume_count = euvo.get_old_unattached_volumes(ec2, ct, report_date,
                                                                             profile_name, region_name)
    print(f'   Number of unattached volumes: {unatt_volume_count}')
    print(f'   Number of valid unattached volumes: {valid_volume_count}')

    print('Getting unused elastic IPs...')
    ip_count = eips.get_old_unattached_eips(ec2, profile_name, region_name)
    print(f'   Number of unattached elastic IPs: {ip_count}')

    return
