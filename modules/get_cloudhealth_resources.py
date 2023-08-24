import requests as req

headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json',
}
params = {
    'per_page': 50
}
client_params = {
    'per_page': 30
}


def get_client_id(client_name, logger):
    client_id = None

    get_customers_response = req.get('https://chapi.cloudhealthtech.com/v1/customers', headers=headers, params=params)
    gcr_json = get_customers_response.json()
    for cust in gcr_json['customers']:
        if cust['name'] == client_name:
            client_id = cust["id"]

    logger.info(f'\n{client_name} ID: {client_id}')

    return client_id


def get_wasted_spend_policy_id(client_name, client_id, logger):
    policy_id = None

    all_policies_response = req.get(f'https://chapi.cloudhealthtech.com/v1/policies?client_api_id={client_id}',
                                    headers=headers, params=client_params)
    apr_json = all_policies_response.json()
    for policy in apr_json['policies']:
        if policy['name'] == ".Wasted Spend":
            policy_id = policy["id"]

    logger.info(f'{client_name} Wasted Spend policy ID: {policy_id}')

    return policy_id


def get_policy_block_ids(client_id, policy_id, logger):
    block_names = ['AWS - EBS Volumes',
                   'AWS - EC2 Snapshots',
                   'AWS - RDS Snapshots',
                   'AWS - Elastic IP Addresses',
                   'AWS - EC2 Image'
                   ]
    block_ids = []

    logger.info('\nGetting block IDs...')

    policy_blocks_response = req.get(f'https://chapi.cloudhealthtech.com/v1/policies/{policy_id}/'
                                     f'policy_blocks?client_api_id={client_id}',
                                     headers=headers, params=client_params)
    pbr_json = policy_blocks_response.json()
    for policy in pbr_json['policy_blocks']:
        policy_name = policy['name']
        if policy_name in block_names:
            block_ids.append(policy['id'])
    logger.info(f'   Block ID list: {block_ids}')

    return block_ids


def get_alert_ids(client_id, policy_id, block_ids, logger):
    alerts_dict = {
        'eip': {
            'ref': 'Elastic IPs unattached',
            'index': 0
        },
        'oldimage': {
            'ref': 'Images are older than',
            'index': 1
        },
        'ebssnaps': {
            'ref': 'Amazon Snapshots are older than',
            'index': 2
        },
        'vol': {
            'ref': 'Volumes unattached greater than',
            'index': 3
        },
        'unami': {
            'ref': 'images have less than',
            'index': 4
        },
        'rdssnaps': {
            'ref': 'RDS Snapshots are older than',
            'index': 5
        }
    }
    alerts_list = [None, None, None, None, None, None]

    logger.info('\nGetting alert IDs...')

    for i in range(len(block_ids)):
        block_id = block_ids[i]

        block_violations_response = req.get(f'https://chapi.cloudhealthtech.com/v1/policies/{policy_id}/'
                                            f'policy_blocks/{block_id}/violations?client_api_id={client_id}',
                                            headers=headers, params=client_params)
        bvr_json = block_violations_response.json()
        for key, value in alerts_dict.items():
            if bvr_json['policy_violations']:
                for violation in bvr_json['policy_violations']:
                    for alert in violation["alerts"]:
                        if value['ref'] in alert["description"]:
                            logger.info(f'   Alert {alert["alert_id"]} for {alert["description"]}')
                            value['block_id'] = block_id
                            value['alert_id'] = alert['alert_id']
            alerts_list[value['index']] = {key: value}

    return alerts_list, alerts_dict


def get_violations(client_id, policy_id, alerts_list, logger):

    logger.info('\nGetting resources that violate Wasted Spend policies...')

    for alert in alerts_list:
        for key, value in alert.items():
            try:
                logger.info(f'Collecting {key} resources...')
                value['affected_resources'] = []

                is_next = None

                while True:
                    if is_next:
                        single_violation_response = req.get(f'https://chapi.cloudhealthtech.com/{is_next["href"]}',
                                                            headers=headers)
                    else:
                        single_violation_response = req.get(f'https://chapi.cloudhealthtech.com/v1/policies/{policy_id}/'
                                                            f'policy_blocks/{value["block_id"]}/violations/'
                                                            f'{value["alert_id"]}?client_api_id={client_id}',
                                                            headers=headers, params=client_params)

                    svr_json = single_violation_response.json()
                    for resource in svr_json['affected_resources']:
                        value['affected_resources'].append(resource)
                    logger.info(f'   {key} resource count: {len(value["affected_resources"])}')

                    try:
                        is_next = svr_json['_links']['next']
                    except KeyError:
                        break
            except KeyError:
                continue

    logger.info('\nAll Cloud Health resources violating Wasted Spend policies have been collected.')
    return alerts_list


# Primary function, returns a list of wasted spend policy alerts and associated resources
def get_cloudhealth_resources(client_name, logger):
    client_id = get_client_id(client_name, logger)
    policy_id = get_wasted_spend_policy_id(client_name, client_id, logger)
    block_ids = get_policy_block_ids(client_id, policy_id, logger)
    alerts_list, alerts_dict = get_alert_ids(client_id, policy_id, block_ids, logger)
    alerts_list_with_resources = get_violations(client_id, policy_id, alerts_list, logger)

    return alerts_list_with_resources, alerts_dict
