#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os, sys,certifi,pymongo
from flask import Flask, request
from pymessenger import Bot
from zmq import Message

#=====================================
client = pymongo.MongoClient("mongodb+srv://test:test@cluster0.jgt9o.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.car
col = db.carlist

app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EAAZAt41d1JvQBAFQHHCM3cKmBgVxV5oUvanFsF2oHjo3lAWCibnmvlZB6BihKahm7mdjzkNAflbD8KWEIKGMb8b9mcG5C19fTz86ttoD7fXbqaazD3gm4MxHZAy5O4CkvwX5EB974VBcQU2RYJy7pVCHE6l6cOUVfjoeUeISB1zZAZASQYEkB"
bot = Bot(PAGE_ACCESS_TOKEN)

price = []
hello = []
carname = []
com_gu={}#留言的留言的ID與Message
com_re=["55","55","55"]#留言的ID與Message
cusdata = {}

num = []
for x in range(1,3500):
    num.append(x)

num1="請輸入購車預算金額:$TWD(萬)最低金額：60萬"
no = "輸入錯誤，請重新輸入!"
carlist = []
datacar = {'價格(萬)': {'$lt': 3500}}
mydata = col.find(datacar) 
for x in mydata:
    a = x["廠牌"]
    b = x["型號"]
    c = x["價格(萬)"]
    d = x["動力"]
    e = x["網址"]
    carlist.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}, 網址:{e}")
    if a not in carname:
        carname.append(a)
    else:
        continue

cusdata = {}
qwe=[]
#=====================================

@app.route('/', methods=['GET'])
def verify():
 # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "just":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200
@app.route('/', methods=['POST'])

def webhook():  
    data = request.get_json()
    log(data)
    print(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                if sender_id not in qwe:
                    qwe.append(sender_id)
                    cusdata[sender_id]={'id':0}
                    cusdata[sender_id]['id']=sender_id
                    print(cusdata)
                if sender_id in qwe:
                    pass
                if messaging_event.get('message'):
                    wel = "歡迎來到0857賞車網:\n以下提供兩種查詢方式 "

                    if 'text' not in cusdata[sender_id]:
                        print('第一次來')
                        cusdata[sender_id]['text']=[]
                        cusdata[sender_id]['text'].append(messaging_event['message']['text'])
                        print(cusdata)
                        buttons=[{
                                "type": "postback",
                                "title": "廠牌查詢",
                                "payload": "aaa"
                            },{ "type": "postback",
                                "title": "預算查詢",
                                "payload": "aaa"}]                    
                        bot.send_button_message(sender_id,wel,buttons)
                    else:
                        cusdata[sender_id]['text'].append(messaging_event['message']['text'])
                        if messaging_event['message']['text'].isdigit():
                            print('預算查詢')
                            cusdata[sender_id]['price']=int(messaging_event['message']['text'])
                            print(cusdata)

                            name = []
                            car = []
                            
                            data = {'價格(萬)': {'$lt':cusdata[sender_id]['price']}}
                            mydata = col.find(data)
                            for result in mydata:
                                a = result["廠牌"]
                                b = result["型號"]
                                c = result["價格(萬)"]
                                d = result["動力"]
                                e = result["網址"]
                                car.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}, 網址:{e}")
                                if a not in name:
                                    name.append(a)
                                else:
                                    continue
                            cusdata[sender_id]['str1']=f"請選擇廠牌：\n{name}"
                            wel2= "若要觀看全部資料,請輸入:全部顯示"
                            bot.send_text_message(cusdata[sender_id]['id'],cusdata[sender_id]['str1'])
                            bot.send_text_message(cusdata[sender_id]['id'],wel2)

                        elif 'price' in cusdata[sender_id]:
                            if messaging_event['message']['text']=="全部顯示":
                                car = []
                                data = {'價格(萬)': {'$lt': cusdata[sender_id]['price']}}
                                mydata = col.find(data)
                                mydata = mydata.sort("價錢(萬)",pymongo.ASCENDING)
                                for result in mydata:
                                    car2 = []
                                    web = []
                                    a = result["廠牌"]
                                    b = result["型號"]
                                    c = result["價格(萬)"] 
                                    d = result["動力"]
                                    e = result["網址"]
                                    web.append(e)
                                    car2.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                    car.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                    buttons =[{"type":"web_url",
                                        "url":f"{e}",
                                        "title":"點我看更多",
                                        "webview_height_ratio": "full"}]
                                    car1=f"清單如下：\n{car2}"
                                    bot.send_button_message(cusdata[sender_id]['id'],car1,buttons)

                                p = len(car)
                                buttons=[{
                                        "type": "postback",
                                        "title": "完成",
                                        "payload": "bbb"
                                    },{ "type": "postback",
                                        "title": "重新查詢",
                                        "payload": "aaa"}]      
                                wel2=f"以上為搜尋結果,共{p}筆\n感謝您的使用"
                                bot.send_button_message(cusdata[sender_id]['id'],wel2,buttons)                            
                            elif  messaging_event['message']['text'] in cusdata[sender_id]['str1']:
                                cusdata[sender_id]['carname']=messaging_event['message']['text']
                                car = []
                                data = {'價格(萬)': {'$lt':cusdata[sender_id]['price']},'廠牌':cusdata[sender_id]['carname']}
                                mydata = col.find(data)
                                mydata = mydata.sort("價錢(萬)", pymongo.ASCENDING)
                                for result in mydata:
                                    car2 = []
                                    web = []
                                    a = result["廠牌"]
                                    b = result["型號"]
                                    c = result["價格(萬)"]
                                    d = result["動力"]
                                    e = result["網址"]
                                    car.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                    car2.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                    web.append(e)
                                    buttons =[{"type":"web_url",
                                        "url":f"{e}",
                                        "title":"點我看更多",
                                        "webview_height_ratio": "full"}]
                                    car1=f"清單如下：\n{car2}"
                                    bot.send_button_message(cusdata[sender_id]['id'],car1,buttons)                        

                                p = len(car)
                                buttons=[{
                                        "type": "postback",
                                        "title": "完成",
                                        "payload": "bbb"
                                    },{ "type": "postback",
                                        "title": "重新查詢",
                                        "payload": "aaa"}]  

                                wel=f"以上為搜尋結果,共{p}筆\n感謝您的使用"
                                bot.send_button_message(cusdata[sender_id]['id'],wel,buttons)

                        elif messaging_event['message']['text'] in str(carname):
                            print('廠牌查詢')
                            cusdata[sender_id]['carname']=messaging_event['message']['text']
                            car = []
                            data = {'廠牌':cusdata[sender_id]['carname']}
                            mydata = col.find(data)
                            mydata = mydata.sort("價錢(萬)", pymongo.ASCENDING)
                            for result in mydata:
                                car2 = []
                                web = []
                                a = result["廠牌"]
                                b = result["型號"]
                                c = result["價格(萬)"]
                                d = result["動力"]
                                e = result["網址"]
                                car.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                car2.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}")
                                web.append(e)
                                buttons =[{"type":"web_url",
                                    "url":f"{e}",
                                    "title":"點我看更多",
                                    "webview_height_ratio": "full"}]
                                car1=f"清單如下：\n{car2}"
                                bot.send_button_message(cusdata[sender_id]['id'],car1,buttons)                        

                            p = len(car)
                            buttons=[{
                                    "type": "postback",
                                    "title": "完成",
                                    "payload": "bbb"
                                },{ "type": "postback",
                                    "title": "重新查詢",
                                    "payload": "aaa"}]  

                            wel=f"以上為搜尋結果,共{p}筆\n感謝您的使用"
                            bot.send_button_message(cusdata[sender_id]['id'],wel,buttons)

                
                
                if messaging_event.get('postback') and str(messaging_event['postback']['title']) == "重新查詢":
                    print("回傳",messaging_event['postback']['title'])
                    
                    wel = "歡迎來到0857賞車網:\n以下提供兩種查詢方式 "
                    buttons=[{
                            "type": "postback",
                            "title": "廠牌查詢",
                            "payload": "aaa"
                        },{ "type": "postback",
                            "title": "預算查詢",
                            "payload": "aaa"}] 
                    bot.send_button_message(cusdata[sender_id]['id'],wel,buttons)   
                if messaging_event.get('postback') and str(messaging_event['postback']['title']) == "廠牌查詢" :
                    print("回傳",messaging_event['postback']['title'])
                    
                    car = []
                    name = []
                    data2 = {'價格(萬)': {'$lt': 3500}}
                    mydata = col.find(data2)
                    for result in mydata:
                        a = result["廠牌"]
                        b = result["型號"]
                        c = result["價格(萬)"]
                        d = result["動力"]
                        e = result["網址"]
                        car.append(f"廠牌:{a}, 型號:{b}, 價格(萬):{c}, 動力:{d}, 網址:{e}")
                        if a not in name:
                            name.append(a)
                        else:
                            continue
                    name1 = f"請選擇廠牌並輸入！廠牌如下：\n{name}"
                    bot.send_text_message(cusdata[sender_id]['id'],name1)
                if messaging_event.get('postback') and str(messaging_event['postback']['title']) == "預算查詢":
                    print("回傳",messaging_event['postback']['title'])
            
                    bot.send_text_message(cusdata[sender_id]['id'],num1)
                if messaging_event.get('postback') and str(messaging_event['postback']['title']) == "再次使用":
                    print("回傳",messaging_event['postback']['title'])
            
                    wel = "歡迎來到0857賞車網:\n以下提供兩種查詢方式 "
                    buttons=[{
                                    "type": "postback",
                                    "title": "廠牌查詢",
                                    "payload": "aaa"
                                },{ "type": "postback",
                                    "title": "預算查詢",
                                    "payload": "aaa"}]                    
                    bot.send_button_message(cusdata[sender_id]['id'],wel,buttons)
                if messaging_event.get('postback') and str(messaging_event['postback']['title']) == "完成":
                    print("回傳",messaging_event['postback']['title'])

                    bye = "感謝您的使用!\n0857賞車網是您最佳選擇!"
                    bot.send_text_message(sender_id,bye)
                    buttons=[{"type": "postback","title": "再次使用","payload": "aaa"}]
                    bye2 = "若要再次使用,請按！"          
                    bot.send_button_message(cusdata[sender_id]['id'],bye2,buttons)
                    
                else:                      
                    messaging_text = 'no text'
            return "ok", 200
def log(message):
    sys.stdout.flush()
if __name__ == "__main__":
    app.run(debug = 0, port = 3000)

