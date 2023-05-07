import csv


def get_unused_images(client, account_name, account_number, region_name, old_images, df_unami):
    """

    :return:
    """

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
    with open(f'{account_name}-{region_name}-unused-images.csv', 'w') as csvfile:
        fields = ['Image Id', 'Image Name']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
            else:
                response = client.describe_images(Owners=[account_number], MaxResults=400)

            images = response['Images']

            # filter criteria:
            # not in use by an existing instance
            # not created by aws backup (AWSBackup in image name)
            # not already in list of old images

            for image in images:
                image_id = image['ImageId']
                image_name = image['Name']

                if image_id not in images_in_use:
                    print(f'   {image_id} is not in use')
                    if image_id in old_images or 'AwsBackup' in image_name:
                        print('      Excluded from results (already an old image or created by AWS Backup.')
                    else:
                        print('      Valid unused image.')
                        unused_images += 1
                        row = [image_id, image_name]
                        writer.writerows([row])

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return df_unami, unused_images
