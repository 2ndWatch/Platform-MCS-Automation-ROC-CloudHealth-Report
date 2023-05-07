import csv


def get_old_unattached_eips(ec2_client, account_name, account_number, region_name, df_eips):
    """

    :return:
    """

    # 'Account Name', 'Account Number', 'Region Name', 'Public IP'

    valid_count = 0
    with open(f'{account_name}-{region_name}-elastic-ips.csv', 'w') as csvfile:
        fields = ['Public IP']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        response = ec2_client.describe_addresses()

        all_ips = response['Addresses']  # list

        for ip in all_ips:
            ip_public = ip['PublicIp']
            if 'AssociationId' in ip.keys():
                continue
            else:
                row = [ip_public]
                writer.writerows([row])
                valid_count += 1

    csvfile.close()

    return df_eips, valid_count
