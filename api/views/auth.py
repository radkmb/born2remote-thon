import json
from flask import Blueprint, request, make_response, jsonify
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from api.models import User
from . import ft_API

session_router = Blueprint('session_router', __name__)

'''
ログイン 参考URL
https://pythonhosted.org/Flask-JWT/
https://qiita.com/y-miine/items/d9f2168fe72a1e29c91f
① /auth にユーザー名とパスワードをdataでPOST。データベースにあれば、トークンが発行される。フロントでCookieとして保持？
② そのトークンをheaderに使えば、ログイン状態となる。
'''

# 実際に認証を行う関数
def authenticate(username, password):
    users = User.getUserListByName()
    user = users.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

# ログインしたユーザーのデータを変数current_identityとして保持
def identity(payload):
    user_id = payload['identity']
    users = User.getUserListByID()
    return users.get(user_id, None)


@session_router.route('/register', methods=['POST'])
def register_user():
    jsonData = json.dumps(request.json)
    userData = json.loads(jsonData)

    ft_id = ft_API.validate_42user(userData['username'])
    if not ft_id:
        return make_response(jsonify({
            'code': 401,
            'data': "{} is not exist in 42 campus.".format(userData['username'])
        }))

    userData['ft_id'] = ft_id
    user = User.registUser(userData)

    if user.get('error'):
        return make_response(jsonify({
            'code': 401,
            'data': user
        }))
    
    return make_response(jsonify({
        'code': 200,
        'data': user
    }))