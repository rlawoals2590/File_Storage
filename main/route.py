from flask import Blueprint, render_template, request, send_file, session
from .User.Func.sign_up import get_users, sing_up, Model, pw_check, update_items, delete_token
from .User.Func.files_up import handle_upload_file, handle_get_file, handle_download_file, handle_delete_file
from .User.Func.user_check import user_validation
from markupsafe import escape
import json
import re

main = Blueprint("route", __name__)


@main.route('/upload', methods=['POST', 'GET'])
@user_validation()
def upload():
    if request.method == 'POST':
        f = request.files['chooseFile']
        user_id = escape(session['user_id'])
        folder_name = get_users(user_id)['Items'][0]['folder_name']

        filename = str(f.filename.replace(" ", '_'))
        try:
            file_info = handle_get_file(folder_name)
            if filename not in file_info:
                f.save('files/' + filename)
                handle_upload_file(filename, folder_name)
                return f'''
                            <script>
                                alert('{filename}이 성공적으로 저장되었습니다!')
                                location.href = '/'
                            </script>
                        '''
            else:
                return f'''
                    <script>
                        alert('{filename}이 이미 저장소에 있습니다!')
                        location.href = '/'
                    </script>
                '''
        except Exception as e:
            error = str(e).lower()
            if 'nonetype' in error:
                filename = str(f.filename.replace(" ", '_'))

                f.save('files/' + filename)
                handle_upload_file(filename, folder_name)
                return f'''
                    <script>
                        alert('{filename}이 성공적으로 저장되었습니다!')
                        location.href = '/'
                    </script>
                '''
            else:
                return '에러 발생', e
    else:
        return render_template('Users/upload.html')


@main.route('/get_files', methods=['GET'])
@user_validation()
def get_files():
    try:
        user_id = escape(session['user_id'])
        folder_name = get_users(user_id)['Items'][0]['folder_name']
        file_info = handle_get_file(folder_name)
        if len(file_info) == 0:
            return '''
                해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 저장하실려면 <a href='/upload'>여기</a>를 눌러 파일을 저장하세요!
            '''
        return render_template('Users/get_files.html', file_info=file_info, user_name=escape(session['user_id']))
    except Exception as e:
        error = str(e).lower()
        if 'nonetype' in error:
            return '''
                해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 저장하실려면 <a href='/upload'>여기</a>를 눌러 파일을 저장하세요!
            '''
        else:
            return '에러 발생', e


@main.route('/download_file', methods=['POST'])
@user_validation()
def download_file():
    file_name = request.form['file_name']
    user_id = escape(session['user_id'])
    folder_name = get_users(user_id)['Items'][0]['folder_name']

    handle_download_file(file_name, folder_name)
    path = f'download/{file_name}'
    return send_file(path, as_attachment=True)


@main.route('/del_file', methods=['POST'])
def del_file():
    file_name = request.form['file_name']
    user_id = escape(session['user_id'])
    folder_name = get_users(user_id)['Items'][0]['folder_name']
    handle_delete_file(file_name, folder_name)
    return f'''
            <script>
                alert('{file_name}이 성공적으로 삭제되었습니다!')
                location.href = '/get_files'
            </script>
        '''
