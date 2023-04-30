import csv


def get_unused_images(client, owner_id, old_images, profile_name, region_name):
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
    with open(f'{profile_name}-{region_name}-unused-images.csv', 'w') as csvfile:
        fields = ['Image Id', 'Image Name']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = client.describe_images(Owners=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                response = client.describe_images(Owners=[owner_id], MaxResults=400)

            images = response['Images']

            # TODO: implement function logic
            # steps:
            # get list of all images (describe_images)
            # filter unused images based on filter criteria below

            # filter criteria:
            # not created by aws backup (AWSBackup in image name)
            # not already in list of old images
            # not deleted by aws backup? (cloudtrail call for DeregisterImage?) - implement after testing first filter
            # and assessing results

            for image in images:
                image_id = image['ImageId']
                image_name = image['Name']

                if image_id not in images_in_use and image_id not in old_images and 'AwsBackup' not in image_name:
                    unused_images += 1
                    row = [image_id, image_name]
                    writer.writerows([row])

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return unused_images
