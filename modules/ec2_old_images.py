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
    :return: list of all old image IDs; list of all EBS snapshot IDs associated with old images
    """
    old_images = []
    image_snapshots = []
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
                image_storage = image['BlockDeviceMappings']
                image_date = image['CreationDate'][:10]
                image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'

                if image_date < cutoff:
                    print(f'   {image_id} is older than 3 months.')
                    if 'AwsBackup' in image_name:
                        print('      Excluded from results (created by AWS Backup).')
                    else:
                        print('      Valid old AMI.')
                        old_images.append(image_id)
                        if image_storage:
                            for device in image_storage:
                                if 'Ebs' in device.keys():
                                    print(f'         {device["Ebs"]["SnapshotId"]} added to list of '
                                          f'image-associated snapshots.')
                                    image_snapshots.append(device['Ebs']['SnapshotId'])
                        row = [image_id, image_name, image_start]
                        writer.writerows([row])

            try:
                is_next = response['NextToken']
            except KeyError:
                break

    csvfile.close()

    return old_images, image_snapshots
