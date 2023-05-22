import boto3
from boto3.dynamodb.conditions import Key
import bcrypt
from config import Config

client = boto3.client('dynamodb',
                      region_name=Config.REGION_NAME)
resource = boto3.resource('dynamodb', region_name=Config.REGION_NAME)
table = resource.Table(Config.TABLE_NAME)


class Model:
    def __init__(self, role=2, **kwargs):
        self.user_id = kwargs['user_id']
        self.folder_name = kwargs['user_id'] + "@" + kwargs['name']
        self.name = kwargs['name']
        self.password = kwargs['password']
        self.role = role

    def pw_encryption(self):
        password = self.password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash = hashed_password.decode('utf-8')
        return password_hash

    def user_model(self):
        password = self.pw_encryption()
        user_info = {
            "user_id": self.user_id,
            "name": self.name,
            "password": password,
            "role": self.role,
            "folder_name": self.folder_name,
            "token": None
        }
        return user_info


def pw_check(user_pw, password):
    return bcrypt.checkpw(user_pw.encode('utf-8'), password.encode('utf-8'))


def get_tables():
    return table


def sing_up(users_info):
    resp = table.put_item(Item=users_info)
    return resp


def get_users(users_id):
    query = {"KeyConditionExpression": Key("user_id").eq(users_id)}
    resp = table.query(**query)
    return resp


def del_users(user_id):
    resp = table.delete_item(
        Key={
            'user_id': user_id
        }
    )
    return resp


def update_items(user_id, token):
    resp = table.update_item(
        Key={
            'user_id': user_id
        },
        AttributeUpdates={
            'token': {
                'Value': token,
                'Action': 'PUT'
            }
        }
    )
    return resp


def delete_token(user_id):
    resp = table.update_item(
        Key={
            'user_id': user_id
        },
        AttributeUpdates={
            'token': {
                'Value': None,
                'Action': 'PUT'
            }
        }
    )
    return resp
