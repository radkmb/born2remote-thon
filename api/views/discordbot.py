from flask import Blueprint, make_response, jsonify
import discord
import re
import datetime
import settings

# .envファイルに設定したbotのトークンを取得
TOKEN = settings.DISCORD_TOKEN
# guild名
GUILD = 'pre_open02_ksuzuki'
# ボイスチャンネルのカテゴリー名
VOICE_CATEGORY = 'クラスター'
# フリーボイスコーナー名
FREE_VOICE_CHANNEL = 'フリーボイス'

# targetがnameと同一人物か判定する
def match_name(name, target):
    if re.match(name+r'(?![a-z])', target):
        return True
    else:
        return False


# チャンネル名を指定してボイスチャンネルを作成して
# フリーボイスからの移動か招待URLを送る
# またサーバーミュートを消す
# (cim = create invite move)
def ft_cim_voice(name):

	# 接続に必要なオブジェクトを生成
	client = discord.Client()
	reply = 0

	# 起動時に動作する処理
	@client.event
	async def on_ready():
		global reply
		# guildを指定
		for guild in client.guilds:
			if guild.name == GUILD:
				break

		# カテゴリーを指定
		category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)

		# member（対象者）を指定
		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

		# 現在時刻を取得してチャンネル名を決めて、チャンネルをカテゴリーにつくる
		now = datetime.datetime.now()
		channel_name = name + '_{0:%d%H%M%S}'.format(now)
		new_channel = await category.create_voice_channel(name=channel_name)

		# memberがFREE_VOICE_CHANNELにいるかどうかで場合分け
		# free_voice → チャンネルをに移動
		# not free_voice → DMで招待URLを送る
		flag = True
		if member.voice:
			if member.voice.channel.name == FREE_VOICE_CHANNEL:
				await member.edit(mute=False, voice_channel=new_channel)
				# '作成と移動が完了した旨のフラグ'
				reply = 1
				flag = False
		if flag:
			invite = await new_channel.create_invite()
			if not member.dm_channel:
				await member.create_dm()
			await member.dm_channel.send(invite)
			# '作成と招待が完了した旨のフラグ'
			reply = 2
		await client.close()

	# Botの起動とDiscordサーバーへの接続
	client.run(TOKEN)
	return reply



# name1 の人が name2の人の席をクリックして
# name2の人のチャンネルの状況により
# ボイスチャンネルを作ったり、招待したりする
def ft_cim_two_voice(name1, name2):

	# 接続に必要なオブジェクトを生成
	client = discord.Client()
	reply = [0, 0]

	# 起動時に動作する処理
	@client.event
	async def on_ready():
		global reply

		# guildを指定
		for guild in client.guilds:
			if guild.name == GUILD:
				break

		# カテゴリーを指定
		category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)

		# memberを指定
		member1 = discord.utils.find(lambda m: match_name(name1, m.name), guild.members)
		member2 = discord.utils.find(lambda m: match_name(name2, m.name), guild.members)

		# member2がクラスターのボイスチャンネルに入ってたらそこにまざり、
		# そうでなかったら自分の部屋を作る
		# flag_make_channel...channelを作る場合Trueになる
		flag_make_channel = True
		if member2.voice:
			if member2.voice.channel:
				if member2.voice.channel.category == category:
					channel = member2.voice.channel
					flag_make_channel = False
		if flag_make_channel:
			now = datetime.datetime.now()
			channel_name = name1 + '_{0:%d%H%M%S}'.format(now)
			channel = await category.create_voice_channel(name=channel_name)

		# member1の処理
		flag = True
		if member1.voice:
			if member1.voice.channel.name == FREE_VOICE_CHANNEL:
				await member1.edit(mute=False, voice_channel=channel)
				# 'member1を移動したフラグ'
				reply[0] = 1
				flag = False
		if flag:
			invite = await channel.create_invite()
			if not member1.dm_channel:
				await member1.create_dm()
			await member1.dm_channel.send(invite)
			# 'member1にDMを送ったフラグ'
			reply[0] = 2

		# member2の処理
		if flag_make_channel:
			flag = True
			if member2.voice:
				if member2.voice.channel.name == FREE_VOICE_CHANNEL:
					await member2.edit(mute=False, voice_channel=channel)
					# 'member1を移動したフラグ'
					reply[1] = 1
					flag = False
			if flag:
				invite = await channel.create_invite()
				if not member2.dm_channel:
					await member2.create_dm()
				await member2.dm_channel.send(invite)
				'member2にDMを送ったフラグ'
				reply[1] = 2
		else:
			reply[1] = -1
		await client.close()

	# Botの起動とDiscordサーバーへの接続
	client.run(TOKEN)
	return reply


# memberを指定してログイン状態を返す
def ft_return_status(name):

	# 接続に必要なオブジェクトを生成
	client = discord.Client()
	reply = 0

	# 起動時に動作する処理
	@client.event
	async def on_ready():
		global reply

		# guildを指定
		for guild in client.guilds:
			if guild.name == GUILD:
				break

		# memberを指定
		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

		if str(member.status) == 'online':
			# 'memberがオンラインであることを表すフラグ'
			reply = 1
		else:
			# 'memberがオンラインではないことをしめすフラグ'
			reply = 0
		await client.close()

	# Botの起動とDiscordサーバーへの接続
	client.run(TOKEN)
	return reply


# フリーボイスに移動させてサーバーミュートにする
def ft_move_freevoice(name):

	# 接続に必要なオブジェクトを生成
	client = discord.Client()
	reply = 0

	# 起動時に動作する処理
	@client.event
	async def on_ready():
		global reply

		# guildを指定
		for guild in client.guilds:
			if guild.name == GUILD:
				break

		# memberを指定
		member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

		# チャンネルを指定
		channel = discord.utils.get(guild.channels, name=FREE_VOICE_CHANNEL)

		# memberをfreevoiceチャンネルに移動する
		reply = 0
		if member.voice:
			if member.voice.channel:
				await member.edit(mute=True, voice_channel=channel)
				# 'freevoiceへの移動が完了したフラグ'
				reply = 1
		await client.close()

	# Botの起動とDiscordサーバーへの接続
	client.run(TOKEN)
	return reply


# 
# 以下Blueprintについて
# 


# Blueprintのオブジェクトを生成する
discordbot = Blueprint('discordbot', __name__)


@discordbot.route('/cim_voice', methods=["GET", "POST"])
@jwt_required()
def cim_voice():
	flag = ft_cim_voice(current_identity.ft_id)
	if flag:
		if flag == 1:
			return make_response(jsonify({
				'flag': '作成と移動が完了した旨のフラグ'
			}))
		else:
			return make_response(jsonify({
				'flag': '作成と招待が完了した旨のフラグ'
			}))
	else:
		return make_response(jsonify({
			'flag': 'エラーが起こった旨のフラグ'
		}))


@discordbot.route('/cim_two_voice', methods=["GET", "POST"])
@jwt_required()
def cim_two_voice():

	jsonData = json.dumps(request.json)
	target = json.loads(jsonData)
	target_name = target['username']

	flag = ft_cim_two_voice(current_identity.ft_id, target_name)

	if flag[0] and flag[1]:
		if flag[1] == -1:
			if flag[0] == 1:
				return make_response(jsonify({
					'flag': 'userの移動が完了した旨のフラグ'
				}))
			else:
				return make_response(jsonify({
					'flag': 'userの招待が完了した旨のフラグ'
				}))
		elif flag[1] == 1:
			if flag[0] == 1:
				return make_response(jsonify({
					'flag': 'チャンネルの作成と、2人のuserの移動が完了した旨のフラグ'
				}))
			else:
				return make_response(jsonify({
					'flag': 'チャンネルの作成と、userの招待、相手の移動が完了した旨のフラグ'
				}))
		else:
			if flag[0] == 1:
				return make_response(jsonify({
					'flag': 'チャンネルの作成と、userの移動、相手の正体が完了した旨のフラグ'
				}))
			else:
				return make_response(jsonify({
					'flag': 'チャンネルの作成と、２人のuserの招待が完了した旨のフラグ'
				}))
	else:
		return make_response(jsonify({
			'flag': 'エラーが起こった旨のフラグ'
	}))


@discordbot.route('/status', methods=["GET", "POST"])
@jwt_required()
def return_status():

	jsonData = json.dumps(request.json)
	target = json.loads(jsonData)
	target_name = target['username']

	flag = ft_return_status(target_name)
	if flag:
		return make_response(jsonify({
			'flag': 'userがオンラインである旨のフラグ'
		}))
	else:
		return make_response(jsonify({
			'flag': 'userがオンラインでない旨のフラグ'
		}))


@discordbot.route('/move_freevoice', methods=["GET", "POST"])
@jwt_required()
def move_freevoice():
	flag = ft_move_freevoice(current_identity.ft_id)
	if flag:
		return make_response(jsonify({
			'flag': 'userをFreeVoiceに移動した旨のフラグ'
		}))
	else:
		return make_response(jsonify({
			'flag': 'userをFreeVoiceに移動できなかった旨のフラグ'
		}))
