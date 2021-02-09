#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
Channel_Access_Token = "/FMRysoNZzP+Hu4ZqqHVbZjJ3OHP0b+B7CLOhrzZ2ZSRCUXzyNP0dwKn/+aTBzHuMLk7z7wv2ST/MkBuSgZCFuXELgLP2xA8028RLE/nRUFxGZiKVLkXnxo78cbnaGIincvUVq4+BsoqFXjuGfJX0wdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(Channel_Access_Token)
# 必須放上自己的Channel Secret
Channel_Secret = "ee9664ace1be9681465425d1ce318147"
handler = WebhookHandler(Channel_Secret)

#User_ID = "@982zkhtz"
#line_bot_api.push_message(User_ID , TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
