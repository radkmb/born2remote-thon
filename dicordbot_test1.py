# インストールした discord.py を読み込む
import discord

# とりあえずBotの色々な操作を試している
# まだBotを介さない方法などは試していない


# 自分のBotのアクセストークンに置き換える
TOKEN = 'token'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    # guildにいるメンバーを出力
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n')

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    # ボイスチャンネルの作成
    if message.content.startswith('/mkch'):
        category_id = message.channel.category_id
        category = message.guild.get_channel(category_id)
        new_channel = await category.create_voice_channel(name='new')
        reply = f'{new_channel.mention} を作成しました'
        await message.channel.send(reply)
    # ボイスチャンネのメンバーリストを出力
    # if message.content.startswith("/voice"):
    #     name = [member.name for member in message.author.voice.channel.members]
    #     if name:
    #         await message.channel.send(name)
    # ボイスチャンネルの招待URLを出力
    if message.content.startswith("/invite"):
        invite = await message.author.voice.channel.create_invite()
        await message.channel.send(invite)
    # 自分のDMに送る
    if message.content.startswith("/mydm"):
        member = message.author
        if not member.dm_channel:
            await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, haha')
    # メンバーのリストを取得して表示
    if message.content == '/members':
        print(message.guild.members)
    # 役職のリストを取得して表示
    if message.content == '/roles':
        print(message.guild.roles)
    # テキストチャンネルのリストを取得して表示
    if message.content == '/text_channels':
        print(message.guild.text_channels)
    # ボイスチャンネルのリストを取得して表示
    if message.content == '/voice_channels':
        print(message.guild.voice_channels)
    # カテゴリチャンネルのリストを取得して表示
    if message.content == '/category_channels':
        print(message.guild.categories)

# メンバーが追加されたときの処理
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


    # ボイスチャンネルの移動

    # if message.content.startswith('/move'):





# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

