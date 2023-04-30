import csv


def get_old_images(client, owner_id, cutoff, profile_name, region_name):
    """
    Gets all images in a region. Writes image properties to a .csv file if an image is older than the cutoff date and
    was not created by AWS Backup.
    :param client: boto3 client obj
    :param owner_id: str
    :param cutoff: str
    :param profile_name: str
    :param region_name: str
    :return: list of all old image IDs; list of valid old image IDs; list of all EBS snapshot IDs associated with old
    images (regardless of whether they were created by AWS Backup)
    """
    all_old_images = []
    image_snapshots = []
    valid_old_images = []
    is_next = None
    with open(f'{profile_name}-{region_name}-old-images.csv', 'w') as csvfile:
        fields = ['Image Id', 'Image Name', 'Image Age']
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        while True:
            if is_next:
                response = client.describe_images(Owners=[owner_id], MaxResults=400, NextToken=is_next)
            else:
                response = client.describe_images(Owners=[owner_id], MaxResults=400)

            images = response['Images']

            for image in images:
                image_id = image['ImageId']
                image_name = image['Name']
                image_storage = image['BlockDeviceMappings']  # list
                image_date = image['CreationDate'][:10]
                image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'

                if image_date < cutoff:
                    all_old_images.append(image_id)
                    if image_storage:
                        for device in image_storage:
                            if 'Ebs' in device.keys():
                                image_snapshots.append(device['Ebs']['SnapshotId'])
                    if 'AwsBackup' not in image_name:
                        valid_old_images.append(image_id)
                        row = [image_id, image_name, image_start]
                        writer.writerows([row])

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return all_old_images, valid_old_images, image_snapshots
