import boto3
from config import Config
from datetime import datetime, timezone
import numpy as np

s3 = boto3.client('s3')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def byte_transform(bytes, bsize=1024):
    r = float(bytes)
    count = 0
    i = r // 1000
    a = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']

    while i != 0.0:
        i = i // 1000
        count += 1

    for i in range(count):
        r = r / bsize
    return str(round(r, 1)) + ' ' + a[count]


def upload_file_time(upload_time):
    upload = utc_to_local(upload_time)
    now = utc_to_local(datetime.utcnow())

    ago_seconds = (now - upload).seconds

    if ago_seconds <= 59:
        return str(ago_seconds) + '초 전'
    elif ago_seconds <= 3599:
        return str(ago_seconds // 60) + '분 전'
    elif ago_seconds <= 86399:
        return str(ago_seconds // 3600) + '시간 전'
    else:
        return str(upload)


def handle_get_file():
    file_list = []
    count = 0
    max_keys = 300
    response = s3.list_objects_v2(Bucket=Config.BUCKET_NAME, MaxKeys=max_keys)

    for content in response.get('Contents'):
        file_name = content.get('Key')
        user_name = file_name.split("/")[0]
        if len(file_name.split("/")[1]) == 0:
            file_name = 'Folder'
        else:
            file_name = file_name.split("/")[1]
        file_size = byte_transform(content.get('Size'))
        file_extension = content.get('Key').split(".")[-1]
        file_upload_time = upload_file_time(content.get('LastModified'))

        file_info = np.array([user_name, file_name, file_size, file_extension, file_upload_time])
        file_list.insert(count, file_info)
        count += 1
    return file_list
