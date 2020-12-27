import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_fsm_graph(reply_token):
	line_bot_api = LineBotApi(channel_access_token)
	line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url="https://jimmy30213.herokuapp.com/show-fsm", preview_image_url="https://jimmy30213.herokuapp.com/show-fsm")) 

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
