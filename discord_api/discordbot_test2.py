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

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

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

    # 名前を指定してdmを送る(前方一致)（二人いるときの処理まだ）
    if message.content.startswith("/namedm"):
        name = message.content.split()[1]
        member = discord.utils.find(lambda m: re.match(name+r'[a-z]*', m.name), guild.members)
        if not member.dm_channel:
            await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, namedm')

    # チャンネル名を指定してボイスチャンネルを作成
    if message.content.startswith("/create_voice"):
        name = message.content.split()[1]
        now = datetime.datetime.now()
        name += '_{0:%d%H%M%S}'.format(now)
        category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
        new_channel = await category.create_voice_channel(name=name)
        reply = f'{new_channel.mention} を作成しました'
        await message.channel.send(reply)

    # チャンネル名を指定してボイスチャンネルを作成して招待も送る(同名処理まだ)
    if message.content.startswith("/ci_voice"):
        name = message.content.split()[1]
        now = datetime.datetime.now()
        channel_name = name + '_{0:%d%H%M%S}'.format(now)
        category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
        new_channel = await category.create_voice_channel(name=channel_name)
        invite = await new_channel.create_invite()
        member = discord.utils.find(lambda m: re.match(name+r'[a-z]*', m.name), guild.members)
        if not member.dm_channel:
            await member.create_dm()
        await member.dm_channel.send(invite)
        reply = f'{new_channel.mention} の作成と招待をしました'
        await message.channel.send(reply)

    # チャンネル名を指定してボイスチャンネルを作成して
    # フリーボイスからの移動か招待URLを送る
    # またサーバーミュートを消す
    if message.content.startswith("/cim_voice"):
        name = message.content.split()[1]
        now = datetime.datetime.now()
        channel_name = name + '_{0:%d%H%M%S}'.format(now)
        category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
        new_channel = await category.create_voice_channel(name=channel_name)
        member = discord.utils.find(lambda m: re.match(name+r'[a-z]*', m.name), guild.members)
        flag = True
        if member.voice:
            if member.voice.channel.name == FREE_VOICE_CHANNEL:
                await member.edit(mute=False, voice_channel=new_channel)
                reply = f'{new_channel.mention} の作成とmemberの移動をしました'
                flag = False
        if flag:
            invite = await new_channel.create_invite()
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(invite)
            reply = f'{new_channel.mention} の作成と招待をしました'
        await message.channel.send(reply)

    # チャンネル名を指定してボイスチャンネルを作成してそのチャンネルに移動させる
    # if message.content.startswith("/pcim_voice"):
    #     name = message.content.split()[1]
    #     now = datetime.datetime.now()
    #     channel_name = name + '_{0:%d%H%M%S}'.format(now)
    #     category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
    #     new_channel = await category.create_voice_channel(name=channel_name)
    #     member = discord.utils.find(lambda m: re.match(name+r'[a-z]*', m.name), guild.members)
    #     await member.edit(voice_channel=new_channel)
    #     reply = f'{new_channel.mention} の作成とmemberの移動をしました'
    #     await message.channel.send(reply)
    # これはできず
    # Target user is not connected to voice.

    # フリーボイスに移動させてサーバーミュートにする
    if message.content.startswith("/m_freevoice"):
        name = message.content.split()[1]
        channel = discord.utils.get(guild.channels, name=FREE_VOICE_CHANNEL)
        member = discord.utils.find(lambda m: re.match(name + r'[a-z]*', m.name), guild.members)
        if member.voice.channel:
            await member.edit(mute=True, voice_channel=channel)
            reply = f'{member.name} をFreeVoiceに移動しました'
        else:
            reply = f'{member.name} Voiceチャンネルにいません'
        await message.channel.send(reply)

    # チャンネル名を指定して消す
    if message.content.startswith("/delete_channel"):
        channel_name = message.content.split()[1]
        channel = discord.utils.get(guild.channels, name=channel_name)
        await channel.delete()
        reply = f'{channel_name} を削除しました'
        await message.channel.send(reply)

    # 特定のカテゴリーの空のチャンネルを削除する
    if message.content.startswith("/ec_delete"):
        category = discord.utils.get(guild.categories, name=VOICE_CATEGORY)
        reply = ''
        for channel in [c for c in category.channels if not c.members]:
            reply += f'{channel.name} '
            await channel.delete()
        if not reply:
            reply = '空のチャンネルはありませんでした'
        else:
            reply += 'を削除しました'
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

    # ボイスチャンネルから移動したらサーバーミュートを解除する
    # if before.mute:
    #     if before.channel:
    #         if before.channel.name == FREE_VOICE_CHANNEL:
    #             if after.channel != before.channel:
    #                 await member.edit(mute=False)
    # これではサーバー離脱したときにエラーがおこる

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