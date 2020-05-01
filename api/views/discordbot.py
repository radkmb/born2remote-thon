# import json
# from flask import Blueprint, make_response, jsonify, request
# from flask_jwt import jwt_required, current_identity
# import discord
# import re
# import datetime
# import settings

# # .envファイルに設定したbotのトークンを取得
# TOKEN = settings.DISCORD_TOKEN
# # guild名
# GUILD = 'pre_open02_ksuzuki'
# # ボイスチャンネルのカテゴリー名
# VOICE_CATEGORY = 'クラスター'
# # フリーボイスコーナー名
# FREE_VOICE_CHANNEL = 'フリーボイス'

# # targetがnameと同一人物か判定する
# def match_name(name, target):
#     if re.match(name+r'(?![a-z])', target):
#         return True
#     else:
#         return False


# client = discord.Client()
# reply = 0
# reply_list = [0, 0]
# ready_flag = 0
# name = ''
# target = ''

# # client起動時に動作する処理
# @client.event
# async def on_ready():

# 	# チャンネル名を指定してボイスチャンネルを作成して
# 	# フリーボイスからの移動か招待URLを送る
# 	# またサーバーミュートを消す
# 	# (cim = create invite move)
# 	if ready_flag == 1:
# 		global reply
# 		# guildを指定
# 		for guild in client.guilds:
# 			if guild.name == GUILD:
# 				break

# 		# カテゴリーを指定
# 		category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)

# 		# member（対象者）を指定
# 		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

# 		# 現在時刻を取得してチャンネル名を決めて、チャンネルをカテゴリーにつくる
# 		now = datetime.datetime.now()
# 		channel_name = name + '_{0:%d%H%M%S}'.format(now)
# 		new_channel = await category.create_voice_channel(name=channel_name)

# 		# memberがFREE_VOICE_CHANNELにいるかどうかで場合分け
# 		# free_voice → チャンネルをに移動
# 		# not free_voice → DMで招待URLを送る
# 		flag = True
# 		if member.voice:
# 			if member.voice.channel.name == FREE_VOICE_CHANNEL:
# 				await member.edit(mute=False, voice_channel=new_channel)
# 				# '作成と移動が完了した旨のフラグ'
# 				reply = 1
# 				flag = False
# 		if flag:
# 			invite = await new_channel.create_invite()
# 			if not member.dm_channel:
# 				await member.create_dm()
# 			await member.dm_channel.send(invite)
# 			# '作成と招待が完了した旨のフラグ'
# 			reply = 2

# 	# name1 の人が name2の人の席をクリックして
# 	# name2の人のチャンネルの状況により
# 	# ボイスチャンネルを作ったり、招待したりする
# 	elif ready_flag == 2:
# 		global reply_list

# 		# guildを指定
# 		for guild in client.guilds:
# 			if guild.name == GUILD:
# 				break

# 		# カテゴリーを指定
# 		category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)

# 		# memberを指定
# 		member1 = discord.utils.find(lambda m: match_name(name, m.name), guild.members)
# 		member2 = discord.utils.find(lambda m: match_name(target, m.name), guild.members)

# 		# member2がクラスターのボイスチャンネルに入ってたらそこにまざり、
# 		# そうでなかったら自分の部屋を作る
# 		# flag_make_channel...channelを作る場合Trueになる
# 		flag_make_channel = True
# 		if member2.voice:
# 			if member2.voice.channel:
# 				if member2.voice.channel.category == category:
# 					channel = member2.voice.channel
# 					flag_make_channel = False
# 		if flag_make_channel:
# 			now = datetime.datetime.now()
# 			channel_name = name + '_{0:%d%H%M%S}'.format(now)
# 			channel = await category.create_voice_channel(name=channel_name)

# 		# member1の処理
# 		flag = True
# 		if member1.voice:
# 			if member1.voice.channel.name == FREE_VOICE_CHANNEL:
# 				await member1.edit(mute=False, voice_channel=channel)
# 				# 'member1を移動したフラグ'
# 				reply_list[0] = 1
# 				flag = False
# 		if flag:
# 			invite = await channel.create_invite()
# 			if not member1.dm_channel:
# 				await member1.create_dm()
# 			await member1.dm_channel.send(invite)
# 			# 'member1にDMを送ったフラグ'
# 			reply_list[0] = 2

# 		# member2の処理
# 		if flag_make_channel:
# 			flag = True
# 			if member2.voice:
# 				if member2.voice.channel.name == FREE_VOICE_CHANNEL:
# 					await member2.edit(mute=False, voice_channel=channel)
# 					# 'member1を移動したフラグ'
# 					reply_list[1] = 1
# 					flag = False
# 			if flag:
# 				invite = await channel.create_invite()
# 				if not member2.dm_channel:
# 					await member2.create_dm()
# 				await member2.dm_channel.send(invite)
# 				'member2にDMを送ったフラグ'
# 				reply_list[1] = 2
# 		else:
# 			reply_list[1] = -1


# 	# memberを指定してログイン状態を返す
# 	elif ready_flag == 3:
# 		global reply

# 		# guildを指定
# 		for guild in client.guilds:
# 			if guild.name == GUILD:
# 				break

# 		# memberを指定
# 		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

# 		if str(member.status) == 'online':
# 			# 'memberがオンラインであることを表すフラグ'
# 			reply = 1
# 		else:
# 			# 'memberがオンラインではないことをしめすフラグ'
# 			reply = 0


# 	# フリーボイスに移動させてサーバーミュートにする
# 	elif ready_flag == 4:
# 		global reply

# 		# guildを指定
# 		for guild in client.guilds:
# 			if guild.name == GUILD:
# 				break

# 		# memberを指定
# 		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

# 		# チャンネルを指定
# 		channel = discord.utils.get(guild.channels, name=FREE_VOICE_CHANNEL)

# 		# memberをfreevoiceチャンネルに移動する
# 		reply = 0
# 		if member.voice:
# 			if member.voice.channel:
# 				await member.edit(mute=True, voice_channel=channel)
# 				# 'freevoiceへの移動が完了したフラグ'
# 				reply = 1


# 	await client.close()



# def ft_cim_voice():
# 	global ready_flag
# 	ready_flag = 1
# 	client.run(TOKEN)

# def ft_cim_two_voice():
# 	global ready_flag
# 	ready_flag = 2
# 	client.run(TOKEN)

# def ft_return_status():
# 	global ready_flag
# 	ready_flag = 3
# 	client.run(TOKEN)


# def ft_move_freevoice():
# 	global ready_flag
# 	ready_flag = 4
# 	client.run(TOKEN)


# #
# # 以下Blueprintについて
# #


# # Blueprintのオブジェクトを生成する
# discordbot = Blueprint('discordbot', __name__)


# @discordbot.route('/cim_voice', methods=["GET", "POST"])
# @jwt_required()
# def cim_voice():
# 	global name
# 	global reply
# 	reply = 0
# 	name = current_identity.ft_id
# 	ft_cim_voice()
# 	if reply:
# 		if reply == 1:
# 			return make_response(jsonify({
# 				'flag': '作成と移動が完了した旨のフラグ'
# 			}))
# 		else:
# 			return make_response(jsonify({
# 				'flag': '作成と招待が完了した旨のフラグ'
# 			}))
# 	else:
# 		return make_response(jsonify({
# 			'flag': 'エラーが起こった旨のフラグ'
# 		}))


# @discordbot.route('/cim_two_voice', methods=["GET", "POST"])
# @jwt_required()
# def cim_two_voice():

# 	jsonData = json.dumps(request.json)
# 	target_user = json.loads(jsonData)

# 	global name
# 	global reply_list
# 	global target
# 	reply_list = [0, 0]
# 	name = current_identity.ft_id
# 	target = target_user['username']

# 	ft_cim_two_voice()

# 	if reply_list[0] and reply_list[1]:
# 		if reply_list[1] == -1:
# 			if reply_list[0] == 1:
# 				return make_response(jsonify({
# 					'flag': 'userの移動が完了した旨のフラグ'
# 				}))
# 			else:
# 				return make_response(jsonify({
# 					'flag': 'userの招待が完了した旨のフラグ'
# 				}))
# 		elif reply_list[1] == 1:
# 			if reply_list[0] == 1:
# 				return make_response(jsonify({
# 					'flag': 'チャンネルの作成と、2人のuserの移動が完了した旨のフラグ'
# 				}))
# 			else:
# 				return make_response(jsonify({
# 					'flag': 'チャンネルの作成と、userの招待、相手の移動が完了した旨のフラグ'
# 				}))
# 		else:
# 			if reply_list[0] == 1:
# 				return make_response(jsonify({
# 					'flag': 'チャンネルの作成と、userの移動、相手の正体が完了した旨のフラグ'
# 				}))
# 			else:
# 				return make_response(jsonify({
# 					'flag': 'チャンネルの作成と、２人のuserの招待が完了した旨のフラグ'
# 				}))
# 	else:
# 		return make_response(jsonify({
# 			'flag': 'エラーが起こった旨のフラグ'
# 	}))


# @discordbot.route('/status', methods=["POST"])
# # @jwt_required()
# def return_status():

# 	jsonData = json.dumps(request.json)
# 	target = json.loads(jsonData)
# 	target_name = target['username']

# 	global name
# 	global reply
# 	reply = 0
# 	name = target_name
# 	ft_return_status()
# 	if reply:
# 		return make_response(jsonify({
# 			'flag': 'userがオンラインである旨のフラグ'
# 		}))
# 	else:
# 		return make_response(jsonify({
# 			'flag': 'userがオンラインでない旨のフラグ'
# 		}))


# @discordbot.route('/move_freevoice', methods=["GET", "POST"])
# @jwt_required()
# def move_freevoice():
# 	global name
# 	global reply
# 	reply = 0
# 	name = current_identity.ft_id
# 	ft_move_freevoice()
# 	if reply:
# 		return make_response(jsonify({
# 			'flag': 'userをFreeVoiceに移動した旨のフラグ'
# 		}))
# 	else:
# 		return make_response(jsonify({
# 			'flag': 'userをFreeVoiceに移動できなかった旨のフラグ'
# 		}))
