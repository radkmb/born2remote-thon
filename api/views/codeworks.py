import json
from flask import Blueprint, request, make_response, jsonify
from flask_jwt import jwt_required, current_identity
from api.models import Codework, CodeworkSchema
from . import ft_API

# ルーティングの設定
codeworks_router = Blueprint('codeworks_router', __name__)

# URLに応じて、各メソッドの実行
@codeworks_router.route('/codeworks', methods=['GET'])
def get_user_list():
    codework = Codework.getCodeList()
    codework_schema = CodeworkSchema(many=True)
    data = codework_schema.dump(codework)
    print(type(data))
    print(data)
    print(data[0]['subject'])
    return make_response(jsonify({
        'code': 200,
        'data': codework_schema.dump(codework)
    }))

@codeworks_router.route('/codeacsess', methods=['GET'])
def get_user_permission():
    projects = ft_API.project_permission('ydoi')

    codework = Codework.getCodeList()
    codework_schema = CodeworkSchema(many=True)
    data = codework_schema.dump(codework)
    l_data = []
    # premission = False
    for l in data:
        if l['subject'] in projects:
            l_data.append(l)
    return make_response(jsonify({
        'code': 200,
        'data': l_data
    }))

@codeworks_router.route('/codeworks', methods=['POST'])
def registUser():

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
    print("User ID: {}".format(current_identity.id))
    print("User Name: {}".format(current_identity.name))
    return make_response(jsonify({
        'id': current_identity.id,
        'name': current_identity.name
    }))