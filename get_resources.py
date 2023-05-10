import boto3
from modules import ec2_old_images as eold
from modules import ec2_old_snapshots as esnap
from modules import rds_old_snapshots as rsnap
from modules import ec2_unused_amis as euna
from modules import ec2_unattached_volumes as euvo
from modules import ec2_elastic_ips as eips


def get_resources(profile, region, report_date, three_month,
                  df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps):
    account_name = profile['account_name']
    region_name = region
    account_number = profile['account_number']

    session = boto3.Session(region_name=region_name)
    ec2 = session.client('ec2')
    rds = session.client('rds')
    ct = session.client('cloudtrail')

    print(f'Starting Cloud Health validation for {account_name} in {region_name}.\n')

    print('Getting unused elastic IPs...')
    df_eips, ip_count = eips.get_old_unattached_eips(ec2, account_name, account_number, region_name, df_eips)
    print(f'   Number of unattached elastic IPs: {ip_count}')

    print('\nGetting EC2 images older than 3 months...')
    df_oldimages, valid_old, img_snaps = eold.get_old_images(ec2, account_name, account_number, region_name,
                                                             three_month, df_oldimages)
    print(f'   Number of valid old images: {len(valid_old)}')
    print(f'   Number of AMI-associated snapshots: {len(img_snaps)}')

    # Dependent on running get_old_images because of img_snaps input
    print('\nGetting EBS snapshots older than 3 months...')
    df_ebssnaps, snapshot_count, valid_snapshot_count = esnap.get_old_snapshots(ec2, account_name, account_number,
                                                                                region_name, img_snaps,
                                                                                three_month, df_ebssnaps)
    print(f'   Number of old EBS snapshots: {snapshot_count}')
    print(f'   Number of valid old EBS snapshots: {valid_snapshot_count}')

    print('\nGetting unattached EC2 volumes...')
    df_vol, unatt_volume_count, valid_volume_count = euvo.get_old_unattached_volumes(ec2, ct, account_name,
                                                                                     account_number, region_name,
                                                                                     report_date, df_vol)
    print(f'   Number of unattached volumes: {unatt_volume_count}')
    print(f'   Number of valid unattached volumes: {valid_volume_count}')

    # Dependent on get_old_images for valid_old input
    print('\nGetting unused EC2 images...')
    df_unami, unused_image_count = euna.get_unused_images(ec2, account_name, account_number, region_name,
                                                          valid_old, three_month, df_unami)
    print(f'   Number of valid unused images: {unused_image_count}')

    print('\nGetting RDS and Aurora snapshots older than 3 months...')
    df_rdssnaps, db_snapshot_count, aurora_snapshot_count = rsnap.get_old_rds_snaps(rds, account_name, account_number,
                                                                                    region_name, three_month,
                                                                                    df_rdssnaps)
    print(f'   Number of valid old RDS snapshots: {db_snapshot_count}')
    print(f'   Number of valid old Aurora snapshots: {aurora_snapshot_count}')

    return df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps
