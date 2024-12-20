# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort
import os,json

from linebot.v3 import (
    WebhookHandler
)

from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    FlexMessage, 
    FlexBubble, 
    FlexBox, 
    FlexText, 
    FlexButton, 
    FlexImage,
    #FlexMessageContainer,
    TextMessage,
    Configuration,
    ImagemapArea,
    ApiClient,
    #CarouselTemplateColumn,
    #ImageCarouselTemplateColumn,
    URIImagemapAction,
    ImagemapBaseSize,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    CarouselTemplate,
    CarouselColumn,
    ImagemapMessage,
    ConfirmTemplate,
    QuickReply,
    QuickReplyItem,
    URIAction,
    PostbackAction,
    MessageAction,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)
app = Flask(__name__)
configuration = Configuration(access_token='9yw71ZXTKe9+K5yIzg/xTUYy05qa/CgcTDbGWmPoORR5vMMd243F3Zmdpps6K0EehZ5+daHPeWkc77nq5uRoQ2LJRX2aAoWnwo+5pM6hymvUcLGBk3UhSMdPkHSoau6fxR5wxiKpG9RpnSFhhPTLqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1c1e2852ed77d82ca01a95e907d95ff6')

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
        if text == '推薦景點':
            carousel_template_columns = [
                CarouselColumn(
                    title='台北101',
                    text='台北市最著名的地標',
                    actions=[
                        URIAction(
                            label='查看詳情',
                            uri='https://www.taipei101.com.tw/'
                        )
                    ]
                ),
                CarouselColumn(
                    title='故宮博物院',
                    text='收藏中國古代文物的博物館',
                    actions=[
                        URIAction(
                            label='官方網站',
                            uri='https://www.npm.gov.tw/'
                        )
                    ]
                ),
                CarouselColumn(
                    title='九份老街',
                    text='懷舊的山城小鎮',
                    actions=[
                        URIAction(
                            label='景點介紹',
                            uri='https://newtaipei.travel/zh-tw/attractions/detail/109990'
                        )
                    ]
                )
            ]

            carousel_template = CarouselTemplate(columns=carousel_template_columns)
            template_message = TemplateMessage(
                alt_text='景點推薦',
                template=carousel_template
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )        
        if text == '推薦餐廳':
            base_url = 'https://github.com/tonywuwutony/line-bot/blob/main/static/food.png?raw=true'
            try:
                # 構建餐廳推薦的 Imagemap
                imagemap_message = ImagemapMessage(
                    base_url=base_url,
                    alt_text='餐廳推薦',
                    base_size=ImagemapBaseSize(height=1040, width=1040),
                    actions=[
                        # 日式料理區域
                        URIImagemapAction(
                            link_uri='https://g.co/kgs/f9NsxdD',
                            area=ImagemapArea(
                                x=0, y=0, width=520, height=520
                            )
                        ),
                        # 西式料理區域
                        URIImagemapAction(
                            link_uri='https://g.co/kgs/xzzqSpz',
                            area=ImagemapArea(
                                x=520, y=0, width=520, height=520
                            )
                        ),
                        # 中式料理區域
                        URIImagemapAction(
                            link_uri='https://g.co/kgs/ocVB9KU',
                            area=ImagemapArea(
                                x=0, y=520, width=520, height=520
                            )
                        ),
                        # 法式料理區域
                        URIImagemapAction(
                            link_uri='https://g.co/kgs/V49uMA3',
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

        elif text == '我要訂餐':
            order_text = '無敵好吃牛肉麵 * 1 ，總價NT200'
            confirm_template = ConfirmTemplate(
                text=order_text,
                actions=[
                    MessageAction(label='確定', text='訂單已確認，謝謝您的購買！'),
                    MessageAction(label='取消', text='已取消訂單，謝謝您的光臨！')
                ]
            )
            template_message = TemplateMessage(
                alt_text='訂單確認',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text=order_text),
                        template_message
                    ]
                )
            )
        elif text == '我想吃飯':
            quick_reply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=MessageAction(label='主菜', text='選擇主菜')
                    ),
                    QuickReplyItem(
                        action=MessageAction(label='湯品', text='選擇湯品')
                    ),
                    QuickReplyItem(
                        action=MessageAction(label='飲料', text='選擇飲料')
                    )
                ]
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(
                            text='請選擇您想要的種類', 
                            quick_reply=quick_reply
                        )
                    ]
                )
            )
        
        elif text == '選擇主菜':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='您已成功將【主菜】加入購物車')
                    ]
                )
            )
        elif text == '選擇湯品':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='您已成功將【湯品】加入購物車')
                    ]
                )
            )
        elif text == '選擇飲料':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='您已成功將【飲料】加入購物車')
                    ]
                )
            )
        elif text == '電影推薦':
            image_carousel_columns = [
                ImageCarouselColumn(
                    image_url='https://github.com/tonywuwutony/line-bot/blob/main/static/772A5BCB-AFA1-4FEA-8A15-46DA4F78596A.jpeg?raw=true',
                    action=URIAction(
                        label='查看詳情',
                        uri='https://www.disneyplus.com/zh-tw/movies/elemental/1B2ZQ9GF35W5'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://github.com/tonywuwutony/line-bot/blob/main/static/A785BADF-002F-4ADA-8161-DB79EE432FE7.jpeg?raw=true',
                    action=URIAction(
                        label='查看詳情',
                        uri='https://zh.wikipedia.org/zh-tw/%E8%85%A6%E7%AD%8B%E6%80%A5%E8%BD%89%E5%BD%8E2'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://github.com/tonywuwutony/line-bot/blob/main/static/67FDAE20-E024-4FBD-B8D9-7EC19677BCDF.jpeg?raw=true',
                    action=URIAction(
                        label='查看詳情',
                        uri='https://www.imdb.com/title/tt0065241/'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://github.com/tonywuwutony/line-bot/blob/main/static/3E174B77-D760-43F3-AA68-A2697C73AA70.jpeg?raw=true',
                    action=URIAction(
                        label='查看詳情',
                        uri='https://www.ambassador.com.tw/home/MovieContent?MID=c3f20454-6f08-4771-a9a1-cbec31812d7e&DT=2024/12/13'
                    )
                )
            ]

            image_carousel_template = ImageCarouselTemplate(columns=image_carousel_columns)
            template_message = TemplateMessage(
                alt_text='電影推薦',
                template=image_carousel_template
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        elif text == '查看菜單':
            menu_json={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://github.com/tonywuwutony/line-bot/blob/main/static/%E7%82%92%E9%A3%AF.jpg?raw=true",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                },
                "contents": [
                {
                    "type": "text",
                    "text": "炒飯",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://developers-resource.landpress.line.me/fx/img/restaurant_regular_32.png"
                        },
                        {
                            "type": "text",
                            "text": "$200",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "好吃的炒飯",
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "xxs"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "xxl",
                    "action": {
                    "type": "postback",
                    "label": "訂購",
                    "data": "已加入購物車",
                    "displayText": "已加入購物車"
                    }
                }
                ]
            }
            }

            menu1_json={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://github.com/tonywuwutony/line-bot/blob/main/static/%E7%82%92%E9%BA%B5.jpg?raw=true",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                },
                "contents": [
                {
                    "type": "text",
                    "text": "炒麵",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://developers-resource.landpress.line.me/fx/img/restaurant_regular_32.png"
                        },
                        {
                            "type": "text",
                            "text": "$200",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "好吃的炒麵",
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "xxs"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "xxl",
                    "action": {
                    "type": "postback",
                    "label": "訂購",
                    "data": "已加入購物車",
                    "displayText": "已加入購物車"
                    }
                }
                ]
            }
            }
            menu2_json={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://github.com/tonywuwutony/line-bot/blob/main/static/%E7%87%B4%E9%A3%AF.jpg?raw=true",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                },
                "contents": [
                {
                    "type": "text",
                    "text": "燴飯",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://developers-resource.landpress.line.me/fx/img/restaurant_regular_32.png"
                        },
                        {
                            "type": "text",
                            "text": "$200",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "好吃的燴飯",
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "xxs"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "xxl",
                    "action": {
                    "type": "postback",
                    "label": "訂購",
                    "data": "已加入購物車",
                    "displayText": "已加入購物車"
                    }
                }
                ]
            }
            }

            menu3_json={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://github.com/tonywuwutony/line-bot/blob/main/static/%E6%BB%B7%E8%82%89%E9%A3%AF.jpg?raw=true",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                },
                "contents": [
                {
                    "type": "text",
                    "text": "滷肉飯",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://developers-resource.landpress.line.me/fx/img/restaurant_regular_32.png"
                        },
                        {
                            "type": "text",
                            "text": "$200",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "好吃的滷肉飯",
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "xxs"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "xxl",
                    "action": {
                    "type": "postback",
                    "label": "訂購",
                    "data": "已加入購物車",
                    "displayText": "已加入購物車"
                    }
                }
                ]
            }
            }
            menu_string = {
                "type": "carousel",
                "contents": [
                    json.loads(json.dumps(menu_json)),
                    json.loads(json.dumps(menu1_json)),
                    json.loads(json.dumps(menu2_json)),
                    json.loads(json.dumps(menu3_json))
                ]
            }
            flex_message = FlexMessage(
            alt_text="菜單",
            contents=FlexContainer.from_json(json.dumps(menu_string))
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

import os
if __name__ == "__main__":
    print("start")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
