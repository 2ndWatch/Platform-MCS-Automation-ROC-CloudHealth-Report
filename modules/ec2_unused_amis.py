def get_unused_images(client, account_name, account_number, region_name, old_images, df_unami):

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

    print(f'   There are {len(images_in_use)} AMIs in use.')

    unused_images = 0

    is_next = None

    while True:
        if is_next:
            response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_images(Owners=[account_number], MaxResults=400)

        images = response['Images']

        # filter criteria:
        # not in use by an existing instance
        # not already in list of old images

        for image in images:
            image_id = image['ImageId']
            image_name = image['Name']

            if image_id not in images_in_use:
                print(f'   {image_id} is not in use')
                if image_id in old_images:
                    print('      Excluded from results (already an old image.')
                else:
                    print('      Valid unused image.')
                    unused_images += 1
                    # 'Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name'
                    row = [account_name, account_number, region_name, image_id, image_name]
                    df_unami.loc[len(df_unami)] = row

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    # print(f'\n{df_unami}\n')

    return df_unami, unused_images
