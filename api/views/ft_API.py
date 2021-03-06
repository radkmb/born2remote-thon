# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_API.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mfunyu <mfunyu@student.42tokyo.jp>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/04/28 14:47:57 by mfunyu            #+#    #+#              #
#    Updated: 2020/04/30 14:54:12 by mfunyu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# アクセストークンの取得
import requests
import settings

client_id = settings.FT_CLIENT_UID
client_secret = settings.FT_CLIENT_SECRET
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

def ft_API(url, payload):
	response = requests.get(url, headers=headers, params=payload)
	if response.status_code != 200:
		exit()
	result = response.json()

	return result


# ユーザーがアクセス権を持つ課題を全て列挙
# user = 'login ID'
# [戻り値 = 課題名のリスト]
def project_permission(user):

	url = 'https://api.intra.42.fr/v2/users/{}/projects_users'.format(user)
	payload = {}

	l_result = ft_API(url, payload)

	projects = []
	for l in l_result:
		if l['status'] == 'finished' and (l['final_mark'] >= 100 or l['retriable_at'] == None or l['cursus_ids'][0] == 9):
			projects.append(l['project']['name'])
	return projects

# Piscine Reloadedの課題全てを取得
# [戻り値 = [プロジェクト名のリスト]]
def all_projects():
	# 全ての課題を表示できる
	url = 'https://api.intra.42.fr/v2/projects'

	# Piscine Reloadedの課題全て
	payload ={'page[size]': 100, 'cursus_id': [28]}
	projects = [l['name'] for l in ft_API(url, payload)]
	# C Piscineの課題全て
	payload ={'page[size]': 100, 'cursus_id': [9]}
	projects += [l['name'] for l in ft_API(url, payload)]

	return projects


def validate_42user(username):
	# return int: ft_id
	url = 'https://api.intra.42.fr/v2/users'
	payload = {'filter[login]': username}
	users = ft_API(url, payload)
	if len(users) == 1:
		id = users[0]['id']
		return id
	else:
		return None