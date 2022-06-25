# 等級機器人

> 如何設置 

</br>

1.  開啟`config.json`
2.  填入 `owner-id` `prefix` `token`
</br></br>
> config.json各項設置

</br>

`owner-id`：擁有者id</br>
`prefix`：機器人前綴</br>
`token`：機器人token</br>
`chat`：聊天相關設置</br>
`chat-cd`：獲得等級的冷卻時間</br>
`chat-max`：單次聊天可以獲得的最高經驗</br>
`chat-min`：單次聊天可以獲得的最低經驗</br>
`chat-blacklist-channel`：沒有辦法獲得等級的頻道
</br></br>
> 各檔案說明

</br>

`bot.py`：最主要的機器人檔案</br>
`config.json`：設定機器人的各種東西</br>
`info.json`：抓資料用</br>
`level.json`：經驗值換等級用 可修改 新增</br>
`rank.json`：紀錄等級用

**注意：等級全群組共用一個.w.**
