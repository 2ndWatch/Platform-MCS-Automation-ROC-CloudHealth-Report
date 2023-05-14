def get_unused_images(client, account_name, account_number, region_name, old_images, cutoff, df_unami, logger):

    # Create list of used AMIs from instance properties
    images_in_use = []
    is_next = None
    while True:
        if is_next:
            response = client.describe_instances(MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_instances(MaxResults=400)

        reservations = response['Reservations']

        for reservation in reservations:
            for instance in reservation['Instances']:
                if 'ImageId' in instance.keys():
                    images_in_use.append(instance['ImageId'])

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    logger.debug(f'   There are {len(images_in_use)} AMIs in use.')

    unused_images = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_images(Owners=[account_number], MaxResults=400)

        images = response['Images']

        # filter criteria:
        # older than 3 months
        # not in use by an existing instance
        # not already in list of old images

        for image in images:
            image_id = image['ImageId']
            try:
                image_name = image['Name']
            except KeyError:
                image_name = ''
            image_date = image['CreationDate'][:10]
            image_storage = image['BlockDeviceMappings']
            storage_size = 0
            # print(f'Creation date: {image_date}')

            if image_date < cutoff:
                if image_id not in images_in_use:
                    logger.debug(f'   {image_id} is not in use')
                    if image_id in old_images:
                        logger.debug('      Excluded from results (already listed in old images).')
                    else:
                        logger.debug('      Valid unused image.')
                        unused_images += 1
                        if image_storage:
                            for device in image_storage:
                                if 'Ebs' in device.keys():
                                    storage_size += device['Ebs']['VolumeSize']
                        # 'Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Storage Size (GB)'
                        row = [account_name, account_number, region_name, image_id, image_name, storage_size]
                        df_unami.loc[len(df_unami)] = row

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    return df_unami, unused_images
