# from flask import Blueprint, session, render_template, request
# import json
# from markupsafe import escape
# from .admin_s3_handler import handle_get_file
#
# admin_main = Blueprint("admin_route", __name__)
#
#
# @admin_main.route('/admin')
# def index():
#     if 'admin_user_name' in session:
#         return render_template('admin/index.html', admin_user_name=escape(session['admin_user_name']))
#     else:
#         return "어드민 계정 등록 및 로그인을 해주세요 <br><a href = '/admin/login'> 로그인 하러가기 </a><br><a href = '/admin/register'> 회원가입 하러가기! "
#
#
# @admin_main.route('/admin/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         admin_user_name = request.form['admin_user_name']
#         for User_name in user_file['Admin']:
#             if admin_user_name in User_name['admin']:
#                 return f'''
#                     <script>
#                         alert('{admin_user_name}님은 이미 등록되어있습니다.')
#                         location.href = '/admin'
#                     </script>
#                 '''
#         admin_user_pw = request.form['admin_user_pw']
#         user_info = {
#             'id': admin_user_name + '@' + admin_user_pw,
#             'admin': admin_user_name,
#             'pw': admin_user_pw,
#             'role': 1
#         }
#
#         user_file['Admin'].append(user_info)
#
#         with open('Users.json', 'w', encoding='utf-8') as make_file:
#             json.dump(user_file, make_file, indent="\t")
#         return f'''
#                     <script>
#                         alert('{admin_user_name}님이 성공적으로 등록되었습니다!')
#                         location.href = '/admin'
#                     </script>
#                 '''
#     else:
#         return render_template('admin/register.html')
#
#
# @admin_main.route('/admin/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         reg_user_name = []
#         reg_user_pw = []
#         admin_user_name = request.form['admin_user_name']
#         admin_user_pw = request.form['admin_user_pw']
#
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         for User_name in user_file['Admin']:
#             reg_user_name.append(User_name['admin'])
#         for User_name in user_file['Admin']:
#             reg_user_pw.append(User_name['pw'])
#
#         if admin_user_name in reg_user_name:
#             if str(admin_user_pw) == str(reg_user_pw[reg_user_name.index(admin_user_name)]):
#                 session['admin_user_name'] = admin_user_name
#                 session['user_role'] = 1
#                 return f'''
#                     <script>
#                         alert('{admin_user_name}님이 성공적으로 로그인되었습니다!')
#                         location.href = '/admin'
#                     </script>
#                 '''
#             else:
#                 return f'''
#                     <script>
#                         alert('비밀번호가 틀렸습니다.')
#                         location.href = '/admin/login'
#                     </script>
#                 '''
#         else:
#             return f'''
#                     <script>
#                         alert('{admin_user_name}님의 아이디가 등록되어있지 않습니다.')
#                         location.href = '/admin/login'
#                     </script>
#                 '''
#     else:
#         return render_template('admin/login.html')
#
#
# @admin_main.route('/admin/get_files')
# def get_files():
#     try:
#         user_file = 'Users.json'
#         with open(user_file, 'r') as user_file:
#             user_file = json.load(user_file)
#
#         file_list = []
#         count = 0
#         session_admin_name = escape(session['admin_user_name'])
#         session_user_role = escape(session['user_role'])
#         for user_name in user_file['Admin']:
#             if session_admin_name == user_name['admin'] and session_user_role == str(user_name['role']):
#                 file_info = handle_get_file()
#                 for a in file_info:
#                     if a[1] != 'Folder':
#                         file_list.insert(count, a)
#                     count += 1
#                 return render_template('admin/get_files.html', file_list=file_list)
#     except Exception as e:
#         error = str(e).lower()
#         if 'nonetype' in error:
#             return '''
#                 해당 저장소에 저장된 파일이 존재하지않습니다.
#             '''
#         else:
#             return '에러 발생', e
#
#
# @admin_main.route('/admin/logout')
# def logout():
#     session.pop('admin_user_name', None)
#     return f'''
#             <script>
#                 alert('로그아웃을 성공하였습니다!')
#                 location.href = '/admin'
#             </script>
#         '''
