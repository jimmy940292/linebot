from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_fsm_graph

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_fsm(self, event):
        reply_token = event.reply_token
        send_fsm_graph(reply_token)
        self.go_back(event);

    def on_exit_fsm(self, event):
        print("Leave fsm")

    def is_going_to_show_channel(self, event):
        text = event.message.text
        return text.lower() == "頻道"

    def on_enter_show_channel(self, event):

        reply_token = event.reply_token
        sending_str =  "NeVeR_LosEs\n" +"nl\n\n" + "羅傑\n" + "roger\n\n"
        send_text_message(reply_token, sending_str)
        self.go_back(event);

    def on_exit_show_channel(self, event):
        print("Leave show_channel")

    def is_going_to_NL_channel(self, event):
        text = event.message.text
        return text.lower() == "nl"

    def on_enter_NL_channel(self, event):

        reply_token = event.reply_token
        sending_str =  "https://www.twitch.tv/never_loses"
        send_text_message(reply_token, sending_str)

    def on_exit_NL_channel(self, event):
        print("Leave NL_channel")

    def is_going_to_NL_information(self, event):
        text = event.message.text
        return text.lower() == "資訊"

    def on_enter_NL_information(self, event):

        reply_token = event.reply_token
        sending_str = "FB:\n"+"https://www.facebook.com/NeVeRLosEs/\n\n" + "IG:\n" + "https://www.instagram.com/nln1nl/\n\n" + "YT:\n" + "https://www.youtube.com/c/NLNL87/featured"
        send_text_message(reply_token, sending_str)
        self.go_back(event)

    def on_exit_NL_information(self, event):
        print("Leave NL_information")

    def is_going_to_Roger_channel(self, event):
        text = event.message.text
        return text.lower() == "roger"

    def on_enter_Roger_channel(self, event):

        reply_token = event.reply_token
        sending_str =  "https://www.twitch.tv/roger9527"
        send_text_message(reply_token, sending_str)

    def on_exit_Roger_channel(self, event):
        print("Leave Roger_channel")

    def is_going_to_Roger_information(self, event):
        text = event.message.text
        return text.lower() == "資訊"

    def on_enter_Roger_information(self, event):

        reply_token = event.reply_token
        sending_str = "FB:\n"+"https://www.facebook.com/Roger95279527/\n\n" + "IG:\n" + "https://www.instagram.com/roger95279527/\n\n"
        send_text_message(reply_token, sending_str)
        self.go_back(event)

    def on_exit_Roger_information(self, event):
        print("Leave Roger_information")
