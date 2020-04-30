from flask import Blueprint
import discord
import re
import datetime

# 自分のBotのアクセストークンに置き換える
TOKEN = 'tokentoken'
# guild名
GUILD = 'pre_open02_ksuzuki'
# ボイスチャンネルのカテゴリー名
VOICE_CATEGORY = 'クラスター'
# フリーボイスコーナー名
FREE_VOICE_CHANNEL = 'フリーボイス'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# targetがnameと同一人物か判定する
def match_name(name, target):
    if re.match(name+r'(?![a-z])', target):
        return True
    else:
        return False

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('ログインしました')

	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# guildにいるメンバーを出力
	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})\n')


# Blueprintのオブジェクトを生成する
discordbot = Blueprint('discordbot', __name__)

# memberのボイスステータスがかわると起動
@client.event
async def on_voice_state_update(member, before, after):
	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# 特定のカテゴリーのチャンネルから離脱したときに
	# そこが空なら削除する
	if before.channel:
		if not before.channel.members:
			category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
			if before.channel.category == category:
				await before.channel.delete()

	# フリーボイスではmute, それ以外ではmuteOffにする
	if member.voice:
		if after.mute:
			if after.channel.name != FREE_VOICE_CHANNEL:
				await member.edit(mute=False)
		else:
			if after.channel.name == FREE_VOICE_CHANNEL:
				await member.edit(mute=True)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

"""
これより上はBot起動に必要なコード
"""


# チャンネル名を指定してボイスチャンネルを作成して
# フリーボイスからの移動か招待URLを送る
# またサーバーミュートを消す
# (cim = create invite move)
@discordbot.route('/discordbot/cim_voice', methods=["GET", "POST"])
def cim_voice(name):

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
	new_channel = category.create_voice_channel(name=channel_name)

	# memberがFREE_VOICE_CHANNELにいるかどうかで場合分け
	# free_voice → チャンネルをに移動
	# not free_voice → DMで招待URLを送る
	flag = True
	if member.voice:
		if member.voice.channel.name == FREE_VOICE_CHANNEL:
			member.edit(mute=False, voice_channel=new_channel)
			# reply = f'{new_channel.mention} の作成とmemberの移動をしました'
			reply = '作成と移動が完了した旨のフラグ'
			flag = False
	if flag:
		invite = new_channel.create_invite()
		if not member.dm_channel:
			member.create_dm()
		member.dm_channel.send(invite)
		# reply = f'{new_channel.mention} の作成と招待をしました'
		reply = '作成と招待が完了した旨のフラグ'
	# message.channel.send(reply)
	return reply




# name1 の人が name2の人の席をクリックして
# name2の人のチャンネルの状況により
# ボイスチャンネルを作ったり、招待したりする
@discordbot.route('/discordbot/cim_two_voice', methods=["GET", "POST"])
def cim_two_voice(name1, name2):

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
		channel = category.create_voice_channel(name=channel_name)

	# member1の処理
	flag = True
	if member1.voice:
		if member1.voice.channel.name == FREE_VOICE_CHANNEL:
			member1.edit(mute=False, voice_channel=channel)
			# reply = f'{channel.mention} の作成とmemberの移動をしました'
			reply = 'member1を移動したフラグ'
			flag = False
	if flag:
		invite = channel.create_invite()
		if not member1.dm_channel:
			member1.create_dm()
		member1.dm_channel.send(invite)
		# reply = f'{channel.mention} の作成と招待をしました'
		reply = 'member1にDMを送ったフラグ'

	# member2の処理
	if flag_make_channel:
		flag = True
		if member2.voice:
			if member2.voice.channel.name == FREE_VOICE_CHANNEL:
				member2.edit(mute=False, voice_channel=channel)
				# reply += f'{channel.mention} の作成とmemberの移動をしました'
				reply += 'member1を移動したフラグ'
				flag = False
		if flag:
			invite = channel.create_invite()
			if not member2.dm_channel:
				member2.create_dm()
			member2.dm_channel.send(invite)
			# reply += f'{channel.mention} の作成と招待をしました'
			reply = 'member2にDMを送ったフラグ'
	# message.channel.send(reply)
	return reply


# memberを指定してログイン状態を返す
@discordbot.route('/discordbot/status', methods=["GET", "POST"])
def return_status(name):

	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# memberを指定
	member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

	if str(member.status) == 'online':
		# reply = f'{member.name} はオンラインです'
		reply = 'memberがオンラインであることを表すフラグ'
	else:
		# reply = f'{member.name} はオフラインです'
		reply = 'memberがオンラインではないことをしめすフラグ'
	# message.channel.send(reply)
	return reply


# フリーボイスに移動させてサーバーミュートにする
@discordbot.route('/discordbot/move_freevoice', methods=["GET", "POST"])
def move_to_fv(name):

	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# memberを指定
	member = discord.utils.find(lambda m: match_name(name, m.name), guild.members)

	# チャンネルを指定
	channel = discord.utils.get(guild.channels, name=FREE_VOICE_CHANNEL)

	# memberをfreevoiceチャンネルに移動する
	flag = True
	if member.voice:
		if member.voice.channel:
			member.edit(mute=True, voice_channel=channel)
			# reply = f'{member.name} をFreeVoiceに移動しました'
			reply = 'freevoiceへの移動が完了したフラグ'
			flag = False
	if flag:
		# reply = f'{member.name} Voiceチャンネルにいません'
		reply = 'freevoiceへの移動ができなかったフラグ'
	# message.channel.send(reply)
	return reply


# 特定のカテゴリーの空のチャンネルを削除する
@discordbot.route('/discordbot/delete_channel', methods=["GET", "POST"])
def delete_channel():

	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# カテゴリーを指定
	category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)

	# 上記カテゴリー内のmemberがいないチャンネルを削除
	for channel in [c for c in category.channels if not c.members]:
		channel.delete()

