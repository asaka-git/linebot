from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pya3rt
import requests

app=Flask(__name__)

#LineBotのインスタンス作成
linebot_api=LineBotApi('GB7s6anlILS56hgylI40UdzoT9SJmXN6JP6uVlc066GGLdkEsRfhY6D9Aywrn+hnInAB536FQMHaS2qD5/JxjddfzJ0i1W6DdEj2wG8bkmIOdpuDj3RAr+dpeedQyBsNhFLYVfPOaEfQIXZIdurSNAdB04t89/1O/w1cDnyilFU=')
#送られてきたメッセージを扱う
handler=WebhookHandler('8a783226480515c98d82a8e8ed87adb5')

#callbackにアクセスが来たら関数を使う
@app.route('/callback',methods=['POST'])
def callback():
  #リクエストがLinePlatformから来ているか確認
  signature=request.headers['X-Line-Signature']
  #リクエストbodyの内容
  body=request.get_data(as_text=True)

  #イベントを処理、tryはplatformからのもの、exceptはそうでないもの
  try:
    handler.handle(body,signature)
  except InvalidSignatureError:
    abort(400)

  return 'OK'

#WebhookHandlerに送られてきたイベントを処理する関数の追加
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
  #来たメッセージの返答する内容
  ai_message=talk_ai(event.message.text)
  #返答する
  linebot_api.reply_message(event.reply_token,TextSendMessage(text=ai_message))

#返事を返す、もしくは検索する
def talk_ai(word):
    if word=="ごりら":
        return 'I AM GORILLA'
    elif word[0]=='Q':
        search_word=word[1:]
        url = 'https://www.google.co.jp/search'
        response = requests.get(url, params={'q':search_word})
        return response.url
    else:
        apikey='DZZgNzc1RdpkDzIvzfq6ZGKJCZ1QH4LL'
        client=pya3rt.TalkClient(apikey)
        reply_message=client.talk(word)
        return reply_message['results'][0]['reply']

  
if __name__=='__main__':
  app.run()


