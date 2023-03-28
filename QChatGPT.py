'''
Date: 2023-03-22 10:18:31
LastEditors: ChocoboQJJ
LastEditTime: 2023-03-28 12:48:09
'''
# -*- coding: utf-8 -*-
 
from flask import Flask, request
import requests
import openai

app = Flask(__name__)
# 这里填入Openai key
openai.api_key = "sk-*****"

@app.route('/', methods=["POST", "GET"])
def post_data():
 
    res = request.get_json()
    # 如果是私聊信息
    if res.get('message_type')=='private':
        # 获取信息发送者的 QQ号码
        qqid = res.get('sender').get('user_id') 
        # 获取原始信息
        message = res.get('raw_message') 
        answer = '不接受私聊哦~'
        
        # 此处解注开启ChatGPT（默认私聊模式下不允许使用ChatGPT）
        # answer = chat(message)
        
        data = {"user_id": qqid,"message": answer,"auto_escape": False}
        url = "http://127.0.0.1:5700/send_private_msg"
        resp = requests.post(url, data=data).text
        print(resp)
        
    # 如果是群聊信息
    if res.get('message_type')=='group':
        print(res)
        # 获取群号
        gid = res.get('group_id') 
        # 获取信息发送者的 QQ号码
        qqid = res.get('sender').get('user_id') 
        # 获取原始信息
        message = res.get('raw_message') 
        message_id = res.get("message_id")
        message_seq = res.get("message_seq")
        answer = message
        # 如果需要设置仅接收到@消息后才进行回复，将xxx改为你的机器人QQ
        if '[CQ:at,qq=xxx]' in answer:
            answer = chat(message[21:])
            data = {"group_id": gid,"message": answer,"auto_escape": False}
            # 此处可以参考Go-Http的官方文档，接口中参数可自行设置
            url = "http://127.0.0.1:5700/send_group_msg"
            resp = requests.post(url, data=data).text
            print(resp)
    return 'OK'

def chat(qq_message):
    response = openai.ChatCompletion.create(
      # 使用gpt3.5turbo模型
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": qq_message}
        ]
    )
    answer = response["choices"][0]["message"]["content"].strip()
    return answer

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5701)# 此处的 host和 port对应上面 yml文件的设置