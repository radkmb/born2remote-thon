from flask import Flask, make_response, jsonify
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from flask_cors import CORS
from .views.codeworks import codeworks_router
from .models.user import User
from api.database import db
import config

def create_app():
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


    app = Flask(__name__)

    # CORS対応
    CORS(app)

    # DBなどの`設定`を読み込む。config.pyで定義
    app.config.from_object('config.Config')
    db.init_app(app)

    # 起動時にtoken, ログイン情報の初期化
    JWT(app, authenticate, identity)

    app.register_blueprint(codeworks_router, url_prefix='/api')

    return app

app = create_app()