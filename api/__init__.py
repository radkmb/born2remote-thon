from flask import Flask, make_response, jsonify
from flask_jwt import JWT, jwt_required
from flask_cors import CORS
# from .views import codeworks_router, session_router, discordbot, authenticate, identity
from .views import codeworks_router, session_router, authenticate, identity
from .models.user import User
from api.database import db
import config
from flask import *


def create_app():

    app = Flask(__name__)

    # CORS対応
    CORS(app)

    # DBなどの`設定`を読み込む。config.pyで定義
    app.config.from_object('config.Config')
    db.init_app(app)

    # 起動時にtoken, ログイン情報の初期化
    JWT(app, authenticate, identity)

    app.register_blueprint(codeworks_router, url_prefix='/api')
    app.register_blueprint(session_router, url_prefix='/session')
    # app.register_blueprint(discordbot, url_prefix='/discordbot')

    return app

app = create_app()

# ホーム画面にアクセスできる
@app.route("/", methods=["GET", "POST"])
# のちに認証を必要にする
# @jwt_required()
def main_page():
    return render_template("index.html")
