from calendar import c
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, QuickReplyButton, QuickReply, MessageAction,
)
import os
from datetime import datetime, timedelta
import re
import weather_api


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

global user_location

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '!頭痛ーる' or event.message.text == '！頭痛ーる':
        line_bot_api.reply_message(
            event.reply_token,
            [
            TextSendMessage(text="位置情報を教えてください。"),
            TextSendMessage(text="https://line.me/R/nv/location/")
            ]
        )
    elif re.compile(r"今日\(\d{1,2}\/\d{1,2}\)").search(event.message.text):
        now = datetime.now()
        today_weather_data = weather_api.get_pressure_status(user_location["city_code"], "today")
        user_location_name = user_location["name"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"今日 {now.month}月{now.day}日 {user_location_name}の気圧情報は\n{today_weather_data}")
        )
    elif re.compile(r"明日\(\d{1,2}\/\d{1,2}\)").search(event.message.text):
        now = datetime.now()
        tomorrow = now + timedelta(1)
        tomorrow_weather_data = weather_api.get_pressure_status(user_location["city_code"], "tommorow")
        user_location_name = user_location["name"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"明日 {tomorrow.month}月{tomorrow.day}日 {user_location_name}の気圧情報は\n{tomorrow_weather_data}")
        )
    elif re.compile(r"明後日\(\d{1,2}\/\d{1,2}\)").search(event.message.text):
        now = datetime.now()
        day_after_tomorrow = now + timedelta(2)
        day_after_tomorrow_weather_data = weather_api.get_pressure_status(user_location["city_code"], "dayaftertomorrow")
        user_location_name = user_location["name"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"明後日 {day_after_tomorrow.month}月{day_after_tomorrow.day}日 {user_location_name}の気圧情報は\n{day_after_tomorrow_weather_data}")
        )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    global user_location
    user_location = weather_api.get_location_info(event.message.address)

    now = datetime.now()
    tomorrow = now + timedelta(1)
    day_after_tomorrow = now + timedelta(2)

    print(event.message.address)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = "日時を指定してください。",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label=f"今日({now.month}/{now.day})", text=f"今日({now.month}/{now.day})")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=f"明日({tomorrow.month}/{tomorrow.day})", text=f"明日({tomorrow.month}/{tomorrow.day})")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=f"明後日({day_after_tomorrow.month}/{day_after_tomorrow.day})", text=f"明後日({day_after_tomorrow.month}/{day_after_tomorrow.day})")
                    ),
                ]
            )
        )
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)