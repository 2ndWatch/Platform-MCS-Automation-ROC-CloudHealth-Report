from modules import ec2_old_images as eold
from modules import ec2_old_snapshots as esnap
from modules import rds_old_snapshots as rsnap
from modules import ec2_unused_amis as euna
from modules import ec2_unattached_volumes as euvo
from modules import ec2_elastic_ips as eips
from botocore.exceptions import ClientError


def get_resources(profile, region, session, today, three_month,
                  df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps, df_ebs_cost, logger):
    account_name = profile['account_name']
    region_name = region
    account_number = profile['account_number']
    valid_old = []
    img_snaps = []
    unauthorized = []

    # Create boto3 clients for EC2, RDS, and CloudTrail
    ec2 = session.client('ec2')
    rds = session.client('rds')
    ct = session.client('cloudtrail')

    logger.info(f'\nStarting Cloud Health validation for {account_name} in {region_name}.\n')

    logger.info('Getting unused elastic IPs...')
    try:
        df_eips, ip_count = eips.get_old_unattached_eips(ec2, account_name, account_number,
                                                         region_name, df_eips, logger)
        logger.info(f'   Number of unattached elastic IPs: {ip_count}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_addresses API call is not authorized in account {account_number} in '
                           f'the {region_name} region.')
            unauthorized.append(['elastic IPs', account_number, region_name])
        else:
            logger.warning(e)

    logger.info('\nGetting EC2 images older than 3 months...')
    try:
        df_oldimages, valid_old, img_snaps = eold.get_old_images(ec2, account_name, account_number, region_name,
                                                                 three_month, df_oldimages, df_ebs_cost, logger)
        logger.info(f'   Number of valid old images: {len(valid_old)}')
        logger.debug(f'   Number of AMI-associated snapshots: {len(img_snaps)}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_images or describe_snapshots API call is not authorized in '
                           f'account {account_number} in the {region_name} region.')
            unauthorized.append(['old images', account_number, region_name])
        else:
            logger.warning(e)

    # Dependent on running get_old_images because of img_snaps input
    logger.info('\nGetting EBS snapshots older than 3 months...')
    try:
        df_ebssnaps, snapshot_count, valid_snapshot_count = esnap.get_old_snapshots(ec2, account_name, account_number,
                                                                                    region_name, img_snaps,
                                                                                    three_month, df_ebssnaps,
                                                                                    df_ebs_cost, logger)
        logger.info(f'   Number of old EBS snapshots: {snapshot_count}')
        logger.info(f'   Number of valid old EBS snapshots: {valid_snapshot_count}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_snapshots API call is not authorized in account {account_number} in '
                           f'the {region_name} region.')
            unauthorized.append(['old EBS snaps', account_number, region_name])
        else:
            logger.warning(e)

    logger.info('\nGetting unattached EC2 volumes...')
    try:
        df_vol, unatt_volume_count, valid_volume_count = euvo.get_old_unattached_volumes(ec2, ct, account_name,
                                                                                         account_number, region_name,
                                                                                         today, df_vol, logger)
        logger.info(f'   Number of unattached volumes: {unatt_volume_count}')
        logger.info(f'   Number of valid unattached volumes: {valid_volume_count}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_volumes API call is not authorized in account {account_number} in '
                           f'the {region_name} region.')
            unauthorized.append(['unatt volumes', account_number, region_name])
        else:
            logger.warning(e)

    # Dependent on get_old_images for valid_old input
    logger.info('\nGetting unused EC2 images...')
    try:
        df_unami, unused_image_count = euna.get_unused_images(ec2, account_name, account_number, region_name,
                                                              valid_old, three_month, df_unami, df_ebs_cost, logger)
        logger.info(f'   Number of valid unused images: {unused_image_count}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_images or describe_snapshots API call is not authorized in '
                           f'account {account_number} in the {region_name} region.')
            unauthorized.append(['unused images', account_number, region_name])
        else:
            logger.warning(e)

    logger.info('\nGetting RDS and Aurora snapshots older than 3 months...')
    try:
        df_rdssnaps, db_snapshot_count, aurora_snapshot_count = rsnap.get_old_rds_snaps(rds, account_name,
                                                                                        account_number, region_name,
                                                                                        three_month, df_rdssnaps,
                                                                                        logger)
        logger.info(f'   Number of valid old RDS snapshots: {db_snapshot_count}')
        logger.info(f'   Number of valid old Aurora snapshots: {aurora_snapshot_count}')
    except ClientError as e:
        if 'UnauthorizedOperation' in str(e):
            logger.warning(f'   The describe_db_snapshots or describe_cluster_snapshots API call is not authorized in '
                           f'account {account_number} in the {region_name} region.')
            unauthorized.append(['RDS snaps', account_number, region_name])
        else:
            logger.warning(e)

    return df_eips, df_oldimages, df_ebssnaps, df_vol, df_unami, df_rdssnaps, unauthorized
