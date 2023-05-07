# import csv


def get_old_images(client, account_name, account_number, region_name, cutoff, df_oldimages):
    """
    Gets all images in a region. Writes image properties to a .csv file if an image is older than the cutoff date and
    was not created by AWS Backup.
    :param df_oldimages:
    :param client: boto3 client obj
    :param account_number: str
    :param cutoff: str
    :param account_name: str
    :param region_name: str
    :return: list of all old image IDs; list of all EBS snapshot IDs associated with old images
    """
    old_images = []
    image_snapshots = []

    is_next = None

    while True:
        if is_next:
            response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
        else:
            response = client.describe_images(Owners=[account_number], MaxResults=400)

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

                    # 'Account Name', 'Account Number', 'Region Name', 'Image Id', 'Image Name', 'Image Age'
                    row = [account_name, account_number, region_name, image_id, image_name, image_start]
                    # df.loc[len(df)] = list
                    df_oldimages.loc[len(df_oldimages)] = row
                    # writer.writerows([row])

        try:
            is_next = response['NextToken']
        except KeyError:
            break

    # with open(f'{account_name}-{region_name}-old-images.csv', 'w') as csvfile:
    #     fields = ['Image Id', 'Image Name', 'Image Age']
    #     writer = csv.writer(csvfile)
    #     writer.writerow(fields)
    #     while True:
    #         if is_next:
    #             response = client.describe_images(Owners=[account_number], MaxResults=400, NextToken=is_next)
    #         else:
    #             response = client.describe_images(Owners=[account_number], MaxResults=400)
    #
    #         images = response['Images']
    #
    #         for image in images:
    #             image_id = image['ImageId']
    #             image_name = image['Name']
    #             image_storage = image['BlockDeviceMappings']
    #             image_date = image['CreationDate'][:10]
    #             image_start = f'{image_date} {image["CreationDate"][11:19]} UTC'
    #
    #             if image_date < cutoff:
    #                 print(f'   {image_id} is older than 3 months.')
    #                 if 'AwsBackup' in image_name:
    #                     print('      Excluded from results (created by AWS Backup).')
    #                 else:
    #                     print('      Valid old AMI.')
    #                     old_images.append(image_id)
    #                     if image_storage:
    #                         for device in image_storage:
    #                             if 'Ebs' in device.keys():
    #                                 print(f'         {device["Ebs"]["SnapshotId"]} added to list of '
    #                                       f'image-associated snapshots.')
    #                                 image_snapshots.append(device['Ebs']['SnapshotId'])
    #                     row = [image_id, image_name, image_start]
    #                     writer.writerows([row])
    #
    #         try:
    #             is_next = response['NextToken']
    #         except KeyError:
    #             break
    #
    # csvfile.close()

    print(f'\n{df_oldimages}\n')

    return df_oldimages, old_images, image_snapshots
