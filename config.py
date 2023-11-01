from datetime import timedelta

class Config:
    REGION_NAME = 'ap-northeast-2'
    TABLE_NAME = 'Users'

    JWT_SECRET_KEY = 'b\'_5#y2L"F4Q8z\n\xec]/'
    SESSION_SECRET_KEY = 'S&DYAUIDH&WFIU82768@$!'
    COOKIE_NAME = 'user_access_token'
    SESSION_LIMIT = timedelta(hours=24)
    ACCESS_TOKEN = timedelta(hours=24)

    BUCKET_NAME = "s3-file-storage-bucket"
