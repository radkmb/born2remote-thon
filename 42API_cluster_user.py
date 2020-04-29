# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    42API_cluster_user.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mfunyu <mfunyu@student.42tokyo.jp>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/04/28 14:47:57 by mfunyu            #+#    #+#              #
#    Updated: 2020/04/29 19:11:46 by mfunyu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# アクセストークンの取得（重複）
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
datap = {
	"grant_type": "client_credentials",
	"client_id": client_id,
	"client_secret": client_secret,
}

auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=datap)
access_token = auth_response.json()["access_token"]
headers = {
		"Authorization": "Bearer {}".format(access_token)
	}

#######################################
# クラスターにログインしているユーザーの取得 #
#######################################
# 引数なしで、　{場所：ユーザー名}　の辞書型を戻す

def cluster_user():
	url = 'https://api.intra.42.fr/v2/campus/26/locations'
	# 100人以上に対応できない
	payload = {'filter[campus_id]': 26, 'page[size]': 100}

	response = requests.get(url, headers=headers, params=payload)
	if response.status_code != 200:
		return "error"
	l_result = response.json()

	location = {}

	for l in l_result:
		#　現在ログインしたままのユーザーを抽出
		if l['end_at'] == None:
			location[l['host']] = l['user']['login']

	return location

# print(cluster_user(url))

