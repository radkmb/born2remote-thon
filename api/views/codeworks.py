import json
from flask import *
from flask_jwt import jwt_required, current_identity
from api.models import Codework, CodeworkSchema
from . import ft_API

# ルーティングの設定
codeworks_router = Blueprint('codeworks_router', __name__)

# URLに応じて、各メソッドの実行
@codeworks_router.route('/codework', methods=['GET'])
@jwt_required()
def display_codework():
    return render_template("codemuseum.html")

@codeworks_router.route('/codeworks', methods=['GET'])
@jwt_required()
def display_codelists():
    projects = get_permitted_codeworks()
    print(projects)
    return render_template("codelist.html", projects=projects)

# ユーザーのアクセス権のあるコードだけが表示される
def get_permitted_codeworks():
    # ユーザーの閲覧可能なプロジェクト全て
    projects = ft_API.project_permission(current_identity.id)

    codework = Codework.getCodeList()
    codework_schema = CodeworkSchema(many=True)

    l_data = []
    # 投稿されているコードから閲覧可能なものを抽出
    for l in codework_schema.dump(codework):
        if l['subject'] in projects:
            l_data.append(l)
    return l_data

@codeworks_router.route('/codeworks', methods=['POST'])
@jwt_required()
def register_codework():

    jsonData = json.dumps(request.json)
    codeData = json.loads(jsonData)

    codework = Codework.registCodework(codeData)
    codework_schema = CodeworkSchema(many=True)

    return make_response(jsonify({
        'code': 200,
        'data': codework
    }))


@codeworks_router.route('/codeworks/protected', methods=['GET'])
@jwt_required()
# @jwt_requiredをすると、ログインしていないと実施できない関数になる。current_identityが使えるから、ユーザー名も拾える
def protected():
    print("User Database ID: {}".format(current_identity.id))
    print("User 42 ID: {}".format(current_identity.ft_id))
    print("User Name: {}".format(current_identity.username))
    return make_response(jsonify({
        'id': current_identity.id,
        'ft_id': current_identity.ft_id,
        'username': current_identity.username
    }))