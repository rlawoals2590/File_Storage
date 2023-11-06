import boto3
from config import Config
from datetime import datetime, timezone
import numpy as np
import re


s3 = boto3.client('s3')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


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


def handle_upload_file(f, folder, extension):  # f = 파일명
    folder_name = folder + "/"
    s3.put_object(Bucket=Config.BUCKET_NAME, Key=folder_name)
    image_extensions = ["jpeg", "jpg", "png", "gif", "bmp", "webp", "svg", "ico", "apng", "avif"]
    if extension in image_extensions:
        local_file_path = f'main/static/img/{f}'
    else:
        local_file_path = f'main/static/files/{f}'
    s3.upload_file(local_file_path, Config.BUCKET_NAME, folder_name + f, ExtraArgs={'ContentType': 'image/jpeg','ACL': 'public-read'})
    return 'Success'


def handle_get_file(folder, sorted):
    file_list = []
    count = 0
    max_keys = 300
    delimiter = "/"
    response = s3.list_objects_v2(Bucket=Config.BUCKET_NAME, Prefix=folder + "/", Delimiter=delimiter, MaxKeys=max_keys)

    for content in response.get('Contents'):
        original_file_name = content.get('Key')
        file_name = original_file_name.replace(folder + "/", "")
        file_size = byte_transform(content.get('Size'))
        file_extension = content.get('Key').split(".")[-1]
        file_upload_time = upload_file_time(content.get('LastModified'))
        file_url = f'https://{Config.BUCKET_NAME}.s3.amazonaws.com/{original_file_name}'

        file_info = np.array([file_name, file_size, file_extension, file_upload_time, file_url])
        file_list.insert(count, file_info)
        count += 1
    file_list = np.delete(file_list, 0, 0)

    if sorted == 'size':
        # sort your files by size
        return  sort_files_by_size(file_list)
    elif sorted == 'time':
        # sort your files by time
        return sort_files_by_time(file_list)
    elif sorted == None:
        return file_list


# 문자열 시간을 초 단위로 변환하는 함수
def time_to_seconds(timestr):
    # 숫자와 시간 단위를 추출 (예: '2분 전' -> ('2', '분'))
    match = re.search(r'(\d+)\s*(\w+)', timestr)
    if match:
        num, unit = match.groups()
        num = int(num)

        # 추출한 단위에 따라 초로 변환
        if '시간' in unit:
            return num * 3600  # 시간을 초로 변환
        elif '분' in unit:
            return num * 60  # 분을 초로 변환
        elif '초' in unit:
            return num  # 초는 그대로
    return 0  # 시간 정보가 없는 경우 또는 알 수 없는 형식의 경우 0초로 처리

# 파일 리스트를 시간 순으로 정렬하는 함수
def sort_files_by_time(file_list):
    # 파일 리스트를 시간에 따라 정렬
    sorted_files = sorted(file_list, key=lambda x: time_to_seconds(x[3]))
    return sorted_files

# 문자열 크기를 바이트 단위로 변환하는 함수
def size_to_bytes(size_str):
    # 단위를 바이트로 변환하는 사전
    unit_to_byte = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
        'PB': 1024**5,
        'EB': 1024**6
    }
    
    match = re.search(r'(\d+(?:\.\d+)?)\s*([A-Z]+)', size_str)
    if match:
        num, unit = match.groups()
        num = float(num)
        if unit in unit_to_byte:
            return num * unit_to_byte[unit]
    return 0  # 크기 정보가 없는 경우 또는 알 수 없는 형식의 경우 0B로 처리

# 파일 리스트를 크기 순으로 정렬하는 함수
def sort_files_by_size(file_list):
    sorted_files = sorted(file_list, key=lambda x: size_to_bytes(x[1]), reverse=True)
    return sorted_files

def handle_download_file(f, folder):
    local_file_path = f'main/download/{f}'
    s3.download_file(Config.BUCKET_NAME, folder + "/" + f, local_file_path)
    return 'Success'


def handle_delete_file(f, folder):
    s3.delete_object(Bucket=Config.BUCKET_NAME, Key=folder + "/" + f)
    return 'Success'
