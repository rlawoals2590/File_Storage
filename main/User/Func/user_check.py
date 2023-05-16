from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps


def user_validation():
    def user_auth_decorator(f):
        @wraps(f)
        @jwt_required(locations=["cookies"], optional=True)
        def _user_auth_decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            if not current_user_id:
                result = '''
                        잘못된 접근입니다. <a href='/'>홈으로</a>이동하셔서 로그인해주세요.
                    '''
                return result
            return f(*args, **kwargs)

        return _user_auth_decorator

    return user_auth_decorator
