# TODO: function for elastic IPs unattached for 4+ weeks (will require CloudTrail API call)
# ec2.describe_addresses
# ct.lookup_events
# needs a wait condition for cloudtrail lookup_events API call (limit two calls per second)

import csv
import datetime
import time


def get_old_unattached_eips(ec2_client, ct_client, report_date, profile_name, region_name):
    """

    :return:
    """
    valid_count = 0
    is_next = None
    with open(f'{profile_name}-{region_name}-elastic-ips.csv', 'w') as csvfile:
        # adding 'Unattached At' field would require an additional call to AWS Config; might be extraneous
        fields = ['Public IP']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                # TODO: check these parameters & token name
                response = ec2_client.describe_addresses(MaxResults=400, NextToken=is_next)
            else:
                response = ec2_client.describe_addresses(MaxResults=400)

            all_ips = response['Addresses']  # list

            # TODO: This may all be wrong. Still researching.
            # for ip in all_ips:
            #     ip_public = ip['PublicIp']
            #     unattached_and_old = True
            #     if 'AssociationId' in ip.keys():
            #         alloc_id = ip['AssociationId']
            #
            #         # TODO: add parameters
            #         ct_response = ct_client.lookup_events()
            #
            #         # TODO: parse response
            #         # yyy = xxx['eventTime'][:10]
            #
            #         # TODO: figure out datetime to subtract 4 weeks from report date
            #         # if event_time > 'report date minus four weeks':
            #         #     unattached_and_old = False
            #
            #         print('   CloudTrail API call for EIP made, waiting 31 seconds...')
            #         time.sleep(31)
            #     if unattached_and_old:
            #         row = [ip_public]
            #         writer.writerows([row])
            #         valid_count += 1

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return