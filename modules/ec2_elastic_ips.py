def get_old_unattached_eips(ec2_client, account_name, account_number, region_name, df_eips):

    valid_count = 0

    response = ec2_client.describe_addresses()
    all_ips = response['Addresses']

    for ip in all_ips:
        ip_public = ip['PublicIp']
        if 'AssociationId' in ip.keys() or 'InstanceId' in ip.keys():
            continue
        else:
            # 'Account Name', 'Account Number', 'Region Name', 'Public IP'
            row = [account_name, account_number, region_name, ip_public]
            df_eips.loc[len(df_eips)] = row
            valid_count += 1

    # print(f'\n{df_eips}\n')

    return df_eips, valid_count
