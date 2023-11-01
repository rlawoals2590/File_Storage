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
                    <script>
                        alert('잘못된 접근입니다! 로그인을 진행해주세요.')
                        location.href = '/login'
                    </script>
                '''
                return result
            return f(*args, **kwargs)

        return _user_auth_decorator

    return user_auth_decorator
