# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    42API_pjt_permission.py                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mfunyu <mfunyu@student.42tokyo.jp>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/04/28 14:47:57 by mfunyu            #+#    #+#              #
#    Updated: 2020/04/29 11:17:48 by mfunyu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests

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

def ft_API(url):
	response = requests.get(url, headers=headers)
	if response.status_code != 200:
		exit()
	l_result = response.json()
	return (l_result)

#############################################
## whether the user has access to the code ##
#############################################

# The assess is allowed when:	The project is in C Pisicne
#								The project is unretriable
#								The user marked >= 100

def project_permission(project_name, user):

	project_id = project_name.lower().replace(' ', '-')
	url = 'https://api.intra.42.fr/v2/users/{}/projects_users'.format(user)

	l_result = ft_API(url)

	if l_result == "error":
		return "error"

	for l in l_result:
		if project_name in l['project']['name']:
			print('<<< "{0}" status >>>\nstatus: {2}\nvalidated?: {3}\nfinal mark: {1}\nretries : {4}\n'.format(project_name, l['final_mark'], l['status'], l['validated?'], 'unretriable' if l['retriable_at'] == None else l['occurrence']))
			if l['status'] == 'finished' and (l['final_mark'] >= 100 or l['retriable_at'] == None or l['cursus_ids'][0] == 9):
				return True
	return False




project_name = ''
# C Piscine C 10
# Piscine Reloaded etc.
user = ''
# login ID

project_permission(project_name, user)
# print(project_permission(project_name, user))
