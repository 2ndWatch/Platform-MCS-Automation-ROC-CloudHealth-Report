def get_old_unattached_eips(ec2_client, account_name, account_number, region_name, df_eips, logger):
    eip_count = 0
    valid_count = 0

    response = ec2_client.describe_addresses()
    all_ips = response['Addresses']
    eip_count += len(all_ips)
    logger.info(f'EIPs found: {eip_count}')

    for ip in all_ips:
        ip_public = ip['PublicIp']
        cost = 3.6
        if 'AssociationId' in ip.keys() or 'InstanceId' in ip.keys():
            continue
        else:
            # 'Account Name', 'Account Number', 'Region Name', 'Public IP', 'Cost Per Month'
            logger.debug(f'   Elastic IP {ip_public} has no associations.')
            row = [account_name, account_number, region_name, ip_public, cost]
            df_eips.loc[len(df_eips)] = row
            valid_count += 1

    return df_eips, valid_count
