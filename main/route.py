from flask import Blueprint, render_template, request, send_file, session
from .User.Func.sign_up import get_users, sing_up, Model, pw_check, update_items, delete_token
from .User.Func.files_up import handle_upload_file, handle_get_file, handle_download_file, handle_delete_file
from .User.Func.user_check import user_validation
from markupsafe import escape
import json
import re

main = Blueprint("route", __name__)

PER_PAGE = 3

@main.route('/upload', methods=['POST', 'GET'])
@user_validation()
def upload():
    if request.method == 'POST':
        f = request.files['file']
        change_filename = request.form['fileName']
        user_id = escape(session['user_id'])
        folder_name = get_users(user_id)['Items'][0]['folder_name']
        if change_filename:
            filename = str(change_filename.replace(" ", '_'))
        else:
            filename = str(f.filename.replace(" ", '_'))
        try:
            file_info = handle_get_file(folder_name, None)
            if filename not in file_info:
                image_extensions = ["jpeg", "jpg", "png", "gif", "bmp", "webp", "svg", "ico", "apng", "avif"]
                file_extension = filename.split('.')[-1]
                if file_extension in image_extensions:
                    f.save('main/static/img/' + filename)
                else:
                    f.save('main/static/files/' + filename)
                handle_upload_file(filename, folder_name, file_extension)
                return f'''
                            <script>
                                alert('{filename}이 성공적으로 저장되었습니다!')
                                location.href = '/get_files'
                            </script>
                        '''
            else:
                return f'''
                    <script>
                        alert('{filename}이 이미 저장소에 있습니다!')
                        location.href = '/upload'
                    </script>
                '''
        except Exception as e:
            error = str(e).lower()
            if 'nonetype' in error:
                filename = str(f.filename.replace(" ", '_'))

                image_extensions = ["jpeg", "jpg", "png", "gif", "bmp", "webp", "svg", "ico", "apng", "avif"]
                file_extension = filename.split('.')[-1]
                if file_extension in image_extensions:
                    f.save('main/static/img/' + filename)
                else:
                    f.save('main/static/files/' + filename)
                handle_upload_file(filename, folder_name, file_extension)
                return f'''
                    <script>
                        alert('{filename}이 성공적으로 저장되었습니다!')
                        location.href = '/get_files'
                    </script>
                '''
            else:
                return '에러 발생', e
    else:
        return render_template('Users/upload.html', user_name=escape(session['user_id']))


@main.route('/get_files', methods=['GET'])
@user_validation()
def get_files():
    try:
        sort = request.args.get('sorted', default=None)

        user_id = escape(session['user_id'])
        folder_name = get_users(user_id)['Items'][0]['folder_name']
        file_info = handle_get_file(folder_name, sort)
        if len(file_info) == 0:
            return '''
                    <script>
                        alert('해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 업로드해주세요!')
                        location.href = '/upload'
                    </script>
                '''
        return render_template('Users/get_files.html', file_info=file_info, user_name=escape(session['user_id']))
    except Exception as e:
        error = str(e).lower()
        if 'nonetype' in error:
            return '''
                    <script>
                        alert('해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 업로드해주세요!')
                        location.href = '/upload'
                    </script>
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
