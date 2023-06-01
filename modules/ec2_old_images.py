def get_old_images(client, account_name, account_number, region_name, cutoff, df_oldimages, df_ebs_cost, logger):
    old_images = []
    image_snapshots = []
    image_count = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_images(Owners=[account_number], MaxResults=400)

        images = response['Images']

        image_count += len(images)
        logger.info(f'Images found: {image_count}')

        for image in images:
            image_id = image['ImageId']
            try:
                image_name = image['Name']
            except KeyError:
                image_name = ''
            image_storage = image['BlockDeviceMappings']
            public = image['Public']
            image_date = image['CreationDate'][:10]
            image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'
            storage_size = 0
            snapshot_count = 0
            storage_cost = 0

            # Filter for images older than 3 months
            if image_date < cutoff:
                logger.debug(f'   {image_id} is older than 3 months.')
                old_images.append(image_id)

                # If the image has one or more associated snapshots, get the snapshot ID(s) and add them to a list
                if image_storage:
                    for device in image_storage:
                        if 'Ebs' in device.keys():
                            snapshot_id = device['Ebs']['SnapshotId']
                            logger.debug(f'         {snapshot_id} added to list of '
                                         f'image-associated snapshots.')
                            storage_size += device['Ebs']['VolumeSize']
                            snapshot_count += 1
                            try:
                                cost = df_ebs_cost.loc[df_ebs_cost['ResourceId'] == snapshot_id,
                                                       'Cost'].values[0].item()
                                storage_cost += cost
                            except IndexError:
                                continue
                            image_snapshots.append(snapshot_id)

                # Note whether the image is public or not
                if public:
                    image_public = 'True'
                else:
                    image_public = 'False'

                # Dataframe column names:
                # 'Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Public',
                # 'Image Age', 'Cost Per Month'
                row = [account_name, account_number, region_name, image_id, image_name, image_public,
                       image_start, round(storage_cost, 2)]
                df_oldimages.loc[len(df_oldimages)] = row

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    return df_oldimages, old_images, image_snapshots
