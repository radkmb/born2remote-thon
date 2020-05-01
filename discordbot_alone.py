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


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は無視する
	if message.author.bot:
		return

	# guildを指定
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# チャンネル名を指定して消す
	if message.content.startswith("/delete_channel"):
		channel_name = message.content.split()[1]
		channel = discord.utils.get(guild.channels, name=channel_name)
		await channel.delete()
		reply = f'{channel_name} を削除しました'
		await message.channel.send(reply)


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

