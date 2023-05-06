import csv


def get_old_unattached_eips(ec2_client, profile_name, region_name):
    """

    :return:
    """
    valid_count = 0
    with open(f'{profile_name}-{region_name}-elastic-ips.csv', 'w') as csvfile:
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

    return valid_count
