def get_unused_images(client, account_name, account_number, region_name, old_images, cutoff,
                      df_unami, df_ebs_cost, logger):
    # Create a list of used AMIs from instance properties
    images_in_use = []
    image_snapshots = []

    is_next = None

    # Generate a list of images in use based on instances
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
    all_images = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_images(Owners=[account_number], MaxResults=400)

        images = response['Images']

        all_images += len(images)
        logger.info(f'Images found: {all_images}')

        # Filter criteria:
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
            public = image['Public']
            storage_size = 0
            snapshot_count = 0
            storage_cost = 0

            # Filter for images older than 3 months
            if image_date < cutoff:

                # Filter for images not in use
                if image_id not in images_in_use:
                    logger.debug(f'   {image_id} is not in use')

                    # Filter for images already in the 'older than 3 months' report
                    if image_id in old_images:
                        logger.debug('      Excluded from results (already listed in old images).')
                    else:
                        logger.debug('      Valid unused image.')
                        unused_images += 1

                        # Calculate storage cost of image snapshots
                        if image_storage:
                            for device in image_storage:
                                if 'Ebs' in device.keys():

                                    # print debugging statement to see response
                                    # logger.info(f'{image_id}: {device["Ebs"]}')

                                    try:
                                        snapshot_id = device['Ebs']['SnapshotId']
                                        logger.debug(f'         {snapshot_id} added to list of '
                                                     f'image-associated snapshots.')
                                        storage_size += device['Ebs']['VolumeSize']
                                        snapshot_count += 1
                                        try:
                                            cost = df_ebs_cost.loc[df_ebs_cost['ResourceId'] == snapshot_id,
                                                                   'Cost'].values[0].item()
                                            # logger.info(f'         {snapshot_id} found, cost: {cost}')
                                            storage_cost += cost
                                        except IndexError:
                                            # logger.info(f'            {snapshot_id} not found in EBS cost table')
                                            continue
                                        image_snapshots.append(snapshot_id)
                                    except KeyError:
                                        logger.debug(f'{image_id}: {device["Ebs"]}')
                                        continue

                        # Note whether the image is public or not
                        if public:
                            image_public = 'True'
                        else:
                            image_public = 'False'

                        # Dataframe column names:
                        # 'Account Name', 'Account Number', 'Region Name', 'Image Id',
                        # 'Image Name', 'Public',  'Cost Per Month'
                        row = [account_name, account_number, region_name, image_id,
                               image_name, image_public, storage_cost]
                        df_unami.loc[len(df_unami)] = row

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    return df_unami, unused_images, image_snapshots
