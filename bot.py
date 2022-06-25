#導入 Discord.py
import datetime
import discord
import json
import random
import os
import requests

#client 是我們與 Discord 連結的橋樑
intents = discord.Intents.default()
client = discord.Client(intents=intents)

with open ("config.json",mode="r") as config:
    config = json.load(config)
prefix = config["prefix"]
owner = config["owner-id"]
token = config["token"]
cd = config["chat"]["cd"]
max = config["chat"]["max"]
min = config["chat"]["min"]
bc = config["chat"]["blacklist-channel"]
now = "1.0.0" #請勿修改 不然你會被機器人叫去更新.w.

r=requests.get('https://raw.githubusercontent.com/peter995peter/rank-bot/main/info.json')
get = r.json()
new = get["version"]

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print("正在檢查版本")
    if now == new:
      print(f"版本檢查完成\n你正在使用最新版({now})!")
    else:
      print(f"版本檢查完成\n你不是使用最新版({new})你正在使用{now}!")
    print('目前登入身份：', client.user)

@client.event
async def on_message(message):
  if message.author.bot != True:
    if message.content == f"{prefix}help":
      await message.channel.send("製作中")
    if message.content == f"{prefix}top":
      top = " "
      with open (f"rank.json") as filt:
        data = json.load(filt)
      nl = 0
      lr = 99999999
      while nl < 10:
        nl += 1
        br = 0
        bi = "無"
        for i in data:
          rank = data[i]["rank"]
          if rank > br and rank < lr:
            br = rank
            bi = i
        with open (f"level.json") as filt:
          data2 = json.load(filt)
        for i in data2:
          if br > data2[i]:
            bl = i
        top = f"{top}\n第{nl}名 <@{bi}> 等級：{bl} 經驗：{br}"
        lr = br
      embed=discord.Embed(title="等級系統",description=top ,color=0xfff105)
      await message.channel.send(embed=embed)
    if message.content.startswith(f"{prefix}rank"):
      if message.mentions == []:
        user = message.author
      else:
        user = message.mentions[0]
      with open (f"rank.json") as filt:
        data = json.load(filt)
      for i in data:
        if i == str(user.id):
          with open (f"level.json") as filt:
            data2 = json.load(filt)
          for i in data2:
            if data[str(user.id)]["rank"] > data2[i]:
              bl = i
          embed=discord.Embed(title="等級系統", description=f'等級：{bl}\n經驗：{data[str(user.id)]["rank"]}', color=0xfff105)
          embed.set_author(name=f"{user}", icon_url=f"{user.avatar_url}")
          await message.channel.send(embed=embed)
          return
      await message.channel.send(f"<@{message.author.id}> 未找到該帳號,請先叫他聊天後再查詢")
    now_time = datetime.datetime.now() - datetime.datetime(1970, 1, 1)
    nt = round(now_time.total_seconds())
    #抓現在時間
    if message.content.startswith(prefix):
      return
    for i in bc:
      if message.channel.id == i:
        return
    with open (f"rank.json") as filt:
      data = json.load(filt)
    for i in data:
      if i == str(message.author.id):
        if data[i]["last-chat"] <= nt - cd:
          gr = random.randrange(min,max)
          data[i]["rank"] = data[i]["rank"] + gr
          data[i]["last-chat"] = nt
      with open (f"rank.json",mode="w") as filt:
        json.dump(data,filt)
      return
    data[str(message.author.id)] = {}
    data[str(message.author.id)]["last-chat"] = 0
    data[str(message.author.id)]["rank"] = 0
    with open (f"rank.json",mode="w") as filt:
        json.dump(data,filt)   

client.run(token)
