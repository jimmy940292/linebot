import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["init","show_channel", "NL_channel", "NL_information", "Roger_channel", "Roger_information"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "show_channel",
            "conditions": "is_going_to_show_channel",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "NL_channel",
            "conditions": "is_going_to_NL_channel",
        },
        {
            "trigger": "detail",
            "source": "NL_channel",
            "dest": "NL_information",
            "conditions": "is_going_to_NL_information",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "Roger_channel",
            "conditions": "is_going_to_Roger_channel",
        },
        {
            "trigger": "detail",
            "source": "Roger_channel",
            "dest": "Roger_information",
            "conditions": "is_going_to_Roger_information",
        },
        {
            "trigger": "go_back",
            "source":  ["show_channel","NL_information","Roger_information"],
            "dest": "init"},
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        if machine.state == "init":
            response = machine.advance(event)
        elif machine.state == "NL_channel" or machine.state == "Roger_channel":
            response = machine.detail(event)

        if response == False:
            send_text_message(event.reply_token, "無效的指令")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
