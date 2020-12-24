from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_show_channel(self, event):
        text = event.message.text
        return text.lower() == "!show"

    def is_going_to_information(self, event):
        text = event.message.text
        return text.lower() == "!info"

    def on_enter_show_channel(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "https://www.twitch.tv/never_loses")

    def on_exit_show_channel(self):
        print("Leaving state1")

    def on_enter_information(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        sending_str = "https://www.facebook.com/NeVeRLosEs/" + "\n\n" + "https://www.instagram.com/nln1nl/" + "\n\n" + "https://www.youtube.com/c/NLNL87/featured"
        send_text_message(reply_token, sending_str)
        self.go_back()

    def on_exit_information(self):
        print("Leaving state2")
