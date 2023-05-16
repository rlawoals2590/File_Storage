# from flask import Blueprint, render_template, request, send_file, session
# from werkzeug.utils import secure_filename
# from .User.Func.files_up import handle_upload_file, handle_get_file, handle_download_file, handle_delete_file
# from markupsafe import escape
# import json
#
# main = Blueprint("route", __name__)
#
#
# @main.route('/')
# def index():
#     if 'user_name' in session:
#         return render_template('users/index.html', user_name=escape(session['user_name']))
#     else:
#         return "회원가입 및 로그인을 해주세요! <br><a href = '/login'> 로그인 하러가기! </a><br><a href = '/register'> 회원가입 하러가기! "
#
#
# @main.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         user_name = request.form['user_name']
#         for User_name in user_file['Users']:
#             if User_name['name'] in user_name:
#                 return f'''
#                     <script>
#                         alert('{user_name}님은 이미 등록되어있습니다.')
#                         location.href = '/'
#                     </script>
#                 '''
#         user_pw = request.form['user_pw']
#         user_info = {
#             'id': user_name + '@' + user_pw,
#             'name': user_name,
#             'pw': user_pw,
#             'folder': user_name,
#             'role': 2
#         }
#
#         user_file['Users'].append(user_info)
#
#         with open('Users.json', 'w', encoding='utf-8') as make_file:
#             json.dump(user_file, make_file, indent="\t")
#         return f'''
#                     <script>
#                         alert('{user_name}님이 성공적으로 등록되었습니다!')
#                         location.href = '/'
#                     </script>
#                 '''
#     else:
#         return render_template('users/register.html')
#
#
# @main.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         reg_user_name = []
#         reg_user_pw = []
#         user_name = request.form['user_name']
#         user_pw = request.form['user_pw']
#
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         for User_name in user_file['Users']:
#             reg_user_name.append(User_name['name'])
#         for User_name in user_file['Users']:
#             reg_user_pw.append(User_name['pw'])
#
#         if user_name in reg_user_name:
#             if user_pw == reg_user_pw[reg_user_name.index(user_name)]:
#                 session['user_name'] = user_name
#                 session['user_role'] = 2
#                 return f'''
#                     <script>
#                         alert('{user_name}님이 성공적으로 로그인되었습니다!')
#                         location.href = '/'
#                     </script>
#                 '''
#         else:
#             return f'''
#                     <script>
#                         alert('{user_name}님의 아이디가 등록되어있지 않습니다.')
#                         location.href = '/'
#                     </script>
#                 '''
#     else:
#         return render_template('users/login.html')
#
#
# @main.route('/logout')
# def logout():
#     session.pop('user_name', None)
#     return f'''
#             <script>
#                 alert('로그아웃을 성공하였습니다!')
#                 location.href = '/'
#             </script>
#         '''
#
#
# @main.route('/upload', methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['chooseFile']
#         try:
#             user_file = 'Users.json'
#             with open(user_file, 'r') as user_file:
#                 user_file = json.load(user_file)
#
#             session_user_name = escape(session['user_name'])
#             session_user_role = escape(session['user_role'])
#             for user_name in user_file['Users']:
#                 if session_user_name == user_name['name'] and session_user_role == str(user_name['role']):
#                     folder_name = user_name['folder']
#                     file_info = handle_get_file(folder_name)
#             if f.filename not in file_info:
#                 f.save('files/' + secure_filename(f.filename))
#                 user_file = 'Users.json'
#
#                 with open(user_file, 'r') as user_file:
#                     user_file = json.load(user_file)
#
#                 session_user_name = escape(session['user_name'])
#                 for user_name in user_file['Users']:
#                     if session_user_name in user_name['name']:
#                         folder_name = user_name['folder']
#                         handle_upload_file(f.filename, folder_name)
#                 return f'''
#                     <script>
#                         alert('{f.filename}이 성공적으로 저장되었습니다!')
#                         location.href = '/'
#                     </script>
#                 '''
#             else:
#                 return f'''
#                     <script>
#                         alert('{f.filename}이 이미 저장소에 있습니다!')
#                         location.href = '/'
#                     </script>
#                 '''
#         except Exception as e:
#             error = str(e).lower()
#             if 'nonetype' in error:
#                 f.save('files/' + secure_filename(f.filename))
#
#                 user_file = 'Users.json'
#                 with open(user_file, 'r') as user_file:
#                     user_file = json.load(user_file)
#
#                 session_user_name = escape(session['user_name'])
#                 for user_name in user_file['Users']:
#                     if session_user_name == user_name['name']:
#                         folder_name = user_name['folder']
#                         handle_upload_file(f.filename, folder_name)
#                 return f'''
#                     <script>
#                         alert('{f.filename}이 성공적으로 저장되었습니다!')
#                         location.href = '/'
#                     </script>
#                 '''
#             else:
#                 return '에러 발생', e
#     else:
#         return render_template('users/upload.html')
#
#
# @main.route('/get_files', methods=['POST', 'GET'])
# def get_files():
#     try:
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         session_user_name = escape(session['user_name'])
#         for user_name in user_file['Users']:
#             if session_user_name == user_name['name']:
#                 folder_name = user_name['folder']
#                 file_info = handle_get_file(folder_name)
#                 if len(file_info) == 0:
#                     return '''
#                         해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 저장하실려면 <a href='/upload'>여기</a>를 눌러 파일을 저장하세요!
#                     '''
#         return render_template('users/get_files.html', file_info=file_info, user_name=escape(session['user_name']))
#     except Exception as e:
#         error = str(e).lower()
#         if 'nonetype' in error:
#             return '''
#                 해당 저장소에 저장된 파일이 존재하지않습니다. 파일을 저장하실려면 <a href='/upload'>여기</a>를 눌러 파일을 저장하세요!
#             '''
#         else:
#             return '에러 발생', e
#
#
# @main.route('/download_file', methods=['POST'])
# def download_file():
#     file_name = request.form['file_name']
#     user_file = 'Users.json'
#     with open(user_file, 'r') as user_file:
#         user_file = json.load(user_file)
#
#     session_user_name = escape(session['user_name'])
#     for user_name in user_file['Users']:
#         if session_user_name == user_name['name']:
#             folder_name = user_name['folder']
#             handle_download_file(file_name, folder_name)
#     path = f'download/{file_name}'
#     return send_file(path, as_attachment=True)
#
#
# @main.route('/del_file', methods=['POST'])
# def del_file():
#     file_name = request.form['file_name']
#     user_file = 'Users.json'
#     with open(user_file, 'r') as user_file:
#         user_file = json.load(user_file)
#
#     session_user_name = escape(session['user_name'])
#     for user_name in user_file['Users']:
#         if session_user_name == user_name['name']:
#             folder_name = user_name['folder']
#             handle_delete_file(file_name, folder_name)
#     return f'''
#             <script>
#                 alert('{file_name}이 성공적으로 삭제되었습니다!')
#                 location.href = '/get_files'
#             </script>
#         '''
