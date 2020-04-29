import json
from flask import Blueprint, request, make_response, jsonify
from api.models import Codework, CodeworkSchema

# ルーティングの設定
codeworks_router = Blueprint('codeworks_router', __name__)

# URLに応じて、各メソッドの実行
@codeworks_router.route('/codeworks', methods=['GET'])
def get_user_list():

    codework = Codework.getCodeList()
    codework_schema = CodeworkSchema(many=True)

    return make_response(jsonify({
        'code': 200,
        'data': codework_schema.dump(codework)
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