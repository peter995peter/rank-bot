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
now = "1.0.0" #請勿修改

r=requests.get('https://raw.githubusercontent.com/peter995peter/rank-bot/main/info.json')
get = r.json()
new = get["version"]

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    print("正在檢查版本")
    if now == new:
      print(f"版本檢查完成\n你正在使用最新版({now})!")
    else:
        print(f"版本檢查完成\n你不是使用最新版({new})你正在使用{now}!\n是否自動更新(https://github.com/HansHans135/sign/blob/main/bot.py 偷來的.w.)")
        i = 1
        while i == 1:
            a = input("你的選擇[y/n]:")
            if a == "y" or a == "n":
                if a == "y":
                    print("下載中...")
                    url = "https://raw.githubusercontent.com/peter995peter/rank-bot/main/bot.py"
                    myfile = requests.get(url)
                    open('bot.py', 'wb').write(myfile.content)
                    print(f"下載完成!!重啟`bot.py`即可生效")
                    i = 0
                if a == "n":
                    print(f"已取消下載")
                    i = 0
            else:
                print("請輸入正確的回答")

@client.event
async def on_message(message):
    for i in bc:
      if messge.chnnel.id == i:
        return
    if message.content == f"{prefix}help":
      await message.channel.send("製作中")
    if message.content == f"{prefix}rank":
      with open (f"rank.json") as filt:
        data = json.load(filt)
      embed=discord.Embed(title="等級系統", description=f'等級：未設置\n經驗：{data[str(message.author.id)]["rank"]}', color=0xfff105)
      embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
      await message.channel.send(embed=embed)
    now_time = datetime.datetime.now() - datetime.datetime(1970, 1, 1)
    nt = round(now_time.total_seconds())
    #抓現在時間
    if message.content.startswith(prefix):
      return
    with open (f"rank.json") as filt:
      data = json.load(filt)
    for i in data:
      if i == str(message.author.id):
        if data[i]["last-chat"] - cd <= nt:
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
