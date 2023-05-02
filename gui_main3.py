from tkinter import *
from tkinter import ttk

import sys
from chatbot.Chatbot import Chatbot
from chatbot.YoutubeToolkit import YoutubeToolkit
from chatbot.NLPTechniques import NLPTechniques
from User import User
import pickle
import re
import textwrap
import html
from urllib.parse import urlparse, parse_qs
import os


# https://www.pythontutorial.net/tkinter/tkinter-thread/

def _check_history():
    files_list = os.listdir('./')
    for file in files_list:
        if file.endswith('.p'):
            return file
    return


class ChatApplication:

    def __init__(self):
        self.topic_name = ''
        self.topic_link = ''
        self.username = ''

        self.openAI = Chatbot()
        self.yt = YoutubeToolkit()
        self.nlp = NLPTechniques()

        self.state = "Name_Received"
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        # Window Configurations
        self.window.title("NLP Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=500, height=500)

        # Text Widget
        self.text_widget = Text(self.window, width=30, height=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Scroll Bar
        self.scrollbar = Scrollbar(self.text_widget)
        self.scrollbar.place(relheight=1, relx=0.974)
        self.scrollbar.configure(command=self.text_widget.yview)

        # Bottom Label
        self.bottom_label = Label(self.window, height=80)
        self.bottom_label.place(relwidth=1, rely=0.825)

        # Message Entry Box
        self.msg_entry = Entry(self.bottom_label)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Send Button
        self.send_button = Button(self.bottom_label, text="Send", width=20, command=lambda: self._on_enter_pressed(None))
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.send_button.configure()

        # Initial Message
        self._insert_message("What's your name?", "Youtube Bot")

    def _on_enter_pressed(self, event):
        user_input = self.msg_entry.get()
        self._insert_message(user_input, "You")
        self._chat_state(self.state, user_input)

    def _chat_state(self, state, user_input):
        match state:
            case "Name_Received":
                self.username = user_input
                self._insert_message("What do you want to discuss?", "Youtube Bot")
                self._insert_message("Please enter JUST the topic or link", "Youtube Bot")
                self.state = "Topic_Verification"
            case "Topic_Verification":
                if re.search("youtu.be\/|youtube.com\/|https", user_input):
                    if self.yt.verify_url(user_input):
                        if not self.yt.verify_comments_enabled(self.yt_get_video_id(urlparse(user_input))):
                            self._insert_message("It seems like the video you've chosen has comment scraping disabled.",
                                                 "Youtube Bot")
                            self._insert_message("Please pick another.", "Youtube Bot")
                        else:
                            self.state = "Topic_Chosen"
                    else:
                        self._insert_message("WHOOPS. Your URL does not seem to work. Please try again or enter a "
                                             "topic.", "Youtube Bot")
                        self._insert_message("Please ensure the link does not contain timestamps or anything after the Video ID.", "Youtube Bot")
                else:
                    videos_link_arr, videos_title_arr = self.yt.get_topic_list(user_input)

                    self._insert_message("Please Pick a Video From The Following Listed Below", "Youtube Bot")
                    displayed_list = ''
                    for num in range(len(videos_title_arr)):
                        displayed_list += str(num + 1) + '. ' + html.unescape(videos_title_arr[num]) + ' | ' + videos_link_arr[num] + '\n'
                    self._insert_message(displayed_list, "Youtube Bot")
                    self._insert_message("Please enter the video integer number.", "Youtube Bot")



    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
