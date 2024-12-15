# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
import re
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImagemapMessage,
    ImagemapBaseSize,
    URIImagemapAction,
    ImagemapArea
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)
configuration = Configuration(access_token='9yw71ZXTKe9+K5yIzg/xTUYy05qa/CgcTDbGWmPoORR5vMMd243F3Zmdpps6K0EehZ5+daHPeWkc77nq5uRoQ2LJRX2aAoWnwo+5pM6hymvUcLGBk3UhSMdPkHSoau6fxR5wxiKpG9RpnSFhhPTLqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1c1e2852ed77d82ca01a95e907d95ff6')

RESTAURANT_LINKS = {
    '日式料理': 'https://g.co/kgs/f9NsxdD',
    '西式料理': 'https://g.co/kgs/xzzqSpz', 
    '中式料理': 'https://g.co/kgs/ocVB9KU',
    '法式料理': 'https://g.co/kgs/V49uMA3'
}



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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        text = event.message.text
        
        if text == '推薦餐廳':
            try:
                # 構建餐廳推薦的 Imagemap
                base_url = request.url_root + 'static/restaurant_imagemap.png'
                base_url = base_url.replace("http://", "https://")
                
                imagemap_message = ImagemapMessage(
                    base_url=base_url,
                    alt_text='餐廳推薦',
                    base_size=ImagemapBaseSize(height=1040, width=1040),
                    actions=[
                        # 日式料理區域
                        URIImagemapAction(
                            link_uri=RESTAURANT_LINKS['日式料理'],
                            area=ImagemapArea(
                                x=0, y=0, width=520, height=520
                            )
                        ),
                        # 西式料理區域
                        URIImagemapAction(
                            link_uri=RESTAURANT_LINKS['西式料理'],
                            area=ImagemapArea(
                                x=520, y=0, width=520, height=520
                            )
                        ),
                        # 中式料理區域
                        URIImagemapAction(
                            link_uri=RESTAURANT_LINKS['中式料理'],
                            area=ImagemapArea(
                                x=0, y=520, width=520, height=520
                            )
                        ),
                        # 法式料理區域
                        URIImagemapAction(
                            link_uri=RESTAURANT_LINKS['法式料理'],
                            area=ImagemapArea(
                                x=520, y=520, width=520, height=520
                            )
                        )
                    ]
                )
                
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[imagemap_message]
                    )
                )
            
            except Exception as e:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"發生錯誤：{str(e)}")]
                    )
                )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
