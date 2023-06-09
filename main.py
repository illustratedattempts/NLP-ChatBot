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

class Main:
    def __init__(self):
        self.prev_user_log = None
        self.chat = Chatbot()
        self.yt = YoutubeToolkit()
        self.nlp = NLPTechniques()
        self.user_name = ""
        self.message_log = []
        self.user_data = None

    def check_if_history_exists(self):
        files_list = os.listdir('./')  # Get List of Files/Directories in Directory | Can be changed to look at
        # different places [LATER]
        for file in files_list:
            if file.endswith('.p'):  # Check if any file has the .p extension
                self.prev_user_log = file
                return True
        return False

    def main_chat(self):
        # We check if this is a new chat instance
        if not self.check_if_history_exists():
            print("Youtube Bot: What's your name?\n")
            potential_user_name = input("User: ")
            print()
            if potential_user_name == '!exit':
                print("Thanks for talking to Youtube Bot :)\n")
                sys.exit(0)
            else:
                self.user_name = potential_user_name
            print("Youtube Bot: Hello ", self.user_name, "!\n", sep='')
            self.user_data = User(self.user_name)
            with open('chat_data.p', 'wb') as f:
                pickle.dump(self.user_data, f)
        else:  # User Data already exists in the directory
            if self.prev_user_log is None:
                print("ERROR!")
                return
            else:
                with open(self.prev_user_log, 'rb') as p:
                    self.user_data = pickle.load(p)
                self.user_name = self.user_data.name  # Need to unpack the user_data username properly
                print("Youtube Bot: Hello, " + self.user_name + "\n")
        self.looping_functionality()

    def looping_functionality(self):
        print("Youtube Bot: **If you want to end the conversation at any time, just say `!exit`**\n")
        print("Youtube Bot: What do you want to discuss?\n")
        while True:
            video_link, video_title = self.topic_verification()  # Will ALWAYS be FORCED to return THIS UNLESS
            while True:  # Confirmation
                print("Youtube Bot: Are you sure you want to look at {}? (Y/N)\n".format(html.unescape(video_title)))
                confirmation_input = input(
                    "{}: ".format(self.user_name)).lower()  # @TODO Need to make it all either caps or lower case [DONE]
                print()
                if confirmation_input == '!exit':
                    print("Thanks for talking to Youtube Bot :)\n")
                    sys.exit(0)
                if confirmation_input == 'y' or confirmation_input == 'yes':
                    break
                elif confirmation_input == 'n' or confirmation_input == 'no':
                    print("Youtube Bot: Alright. Let us try again.\n")
                    video_link, video_title = self.topic_verification()
                else:
                    print("Youtube Bot: Please enter either YES(Y) or NO(N).\n")

            # Prompt to store LIKES/DISLIKES
            self.get_user_likes_and_dislikes(video_title)

            # Assign the chatbot configs using video link
            self.chatbot_configs(video_link)

            # Freed chatbot
            self.freed_chatbot()

            print("Youtube Bot: What else would you like to discuss?\n")

            # @TODO Store user likes/dislikes somehow
            # exiting the ENTIRE PROGRAM after this

    def topic_verification(self):
        """
        The user either enters a URL or topic. If it is not a working URL then we force them to enter a URL or topic.
        Otherwise, we immediately assume it's a topic.
        """
        print("Youtube Bot: Please enter JUST the topic or link.\n")
        # FOR TESTING PURPOSES:
        # self.user_name = 'Tester'
        user_input = input("{}: ".format(self.user_name))
        print()
        if user_input == '!exit':
            print("Thanks for talking to Youtube Bot :)\n")
            sys.exit(0)
        while True:
            if re.search("youtu.be\/|youtube.com\/|https", user_input):  # Check if the user's input has a link
                if self.yt.verify_url(user_input):  # Verify the URL works
                    if not self.yt.verify_comments_enabled(self.yt.get_video_id(urlparse(user_input))):
                        print("Youtube Bot: It seems like the video you've chosen has comment scraping disabled. Please pick another.\n")
                        user_input = input("{}: ".format(self.user_name))
                        print()
                        continue
                    return user_input, self.yt.get_video_name(user_input)
                else:
                    print("Youtube Bot: WHOOPS. Your URL does not seem to work. Please try again or enter a topic.\n")
                    print("Youtube Bot: Please ensure the link does not contain timestamps or anything after the Video ID.\n")
                    user_input = input("{}: ".format(self.user_name))
                    print()
            else:  # VIDEO SEARCH FROM TOPIC
                videos_link_arr, videos_title_arr = self.yt.get_topic_list(user_input)

                print("Youtube Bot: Please Pick a Video From The Following Listed Below.\n")
                for num in range(len(videos_title_arr)):
                    print(str(num + 1) + '. ' + html.unescape(videos_title_arr[num]) + ' | ' + videos_link_arr[num])

                print("\nYoutube Bot: Please enter the video integer number.\n")

                while True:  # Continuous checks to see if the input is correct
                    selected_vid_index = input("{}: ".format(self.user_name))
                    print()
                    if selected_vid_index == '!exit':
                        print("Thanks for talking to Youtube Bot :)\n")
                        sys.exit(0)
                    if selected_vid_index.isdigit():
                        selected_vid_index = int(selected_vid_index)
                        if 0 < selected_vid_index < 6:  # Checks if in the range of 1, 5 inclusive
                            selected_vid_index = selected_vid_index - 1
                            if not self.yt.verify_comments_enabled(self.yt.get_video_id(urlparse(videos_link_arr[selected_vid_index]))):
                                print("Youtube Bot: It seems like the video you've chosen has comment scraping disabled. Please pick another topic.\n")
                                break
                            return videos_link_arr[selected_vid_index], videos_title_arr[selected_vid_index]
                        else:
                            print("Youtube Bot: Please enter a listed video number.\n")
                    else:
                        print("Youtube Bot: Please enter an INTEGER number.\n")
            

    def get_user_likes_and_dislikes(self, video_title):
        video_title_unescape = html.unescape(video_title)
        print("Youtube Bot: What do you like about: {}?\n".format(video_title_unescape))
        user_likes = input("{}: ".format(self.user_name))
        print()
        if user_likes == '!exit':
            print("Thanks for talking to Youtube Bot :)\n")
            sys.exit(0)
        self.user_data.likes.append(user_likes)
        # print("Youtube Bot: Okay.")
        print("Youtube Bot: What do you dislike about {}?\n".format(video_title_unescape))
        user_dislikes = input("{}: ".format(self.user_name))
        print()
        if user_dislikes == '!exit':
            print("Thanks for talking to Youtube Bot :)\n")
            sys.exit(0)
        self.user_data.dislikes.append(user_dislikes)
        with open('chat_data.p', 'wb') as f:
            pickle.dump(self.user_data, f)

    def chatbot_configs(self, link):
        # Get the comments from the video
        comments = self.yt.comment_finder(link)
        # clean_comments type list
        clean_comments = self.nlp.clean_text_array(comments)
        comment_freq = self.nlp.word_frequency(clean_comments)

        # Setup chatbot to discuss current video
        # Give the chatbot the title of the video
        self.message_log.append(
            {"role": "system", "content": "You are a bot that pretends to give analysis on Youtube videos."})
        self.message_log.append({"role": "system",
                                 "content": "You do not need to have knowledge on the videos, just give an analysis based on sentiment score and title."})
        self.message_log.append({"role": "system",
                                 "content": "Also, try to utilize keywords that relate to the video in your response."})
        title_message = "The video you are currently discussing is called " + self.yt.get_video_name(link)
        self.message_log.append({"role": "system", "content": title_message})
        
        # Give the user feedback on the video
        user_likes = "The user likes this about the video " + self.user_data.likes[-1]
        user_dislikes = "The user does not like this about the video " + self.user_data.dislikes[-1]
        self.message_log.append(
            {"role": "system", "content": user_likes})
        self.message_log.append(
            {"role": "system", "content": user_dislikes})

        # Give the chatbot the sentiment analysis of the comments
        sentiment_score = self.nlp.sentiment_analysis(" ".join(comments))
        sentiment_message = "The video you are currently discussing has a sentiment score of " + str(
            sentiment_score[0]) + " percent negative, " + str(sentiment_score[1]) + " percent neutral, and " + str(
            sentiment_score[2]) + " percent positive."
        self.message_log.append({"role": "system", "content": sentiment_message})

        # Give the chatbot the most frequent words in order
        common_words = []
        for key, value in sorted(comment_freq.items(), key=lambda x: x[1], reverse=True):
            common_words.append(key)

        # Send the bot the 100 most common words
        common_words_message = "The most common words commented under the video are "
        for i in range(0, min(len(common_words), 100)):
            common_words_message += common_words[i] + " "
        self.message_log.append({"role": "system", "content": common_words_message})
        self.message_log.append(
            {"role": "system", "content": "Generate your first response, given the information above."})
        bot_message = self.chat.generate_message(self.message_log)
        self.message_log.append({
            "role": "assistant",
            "content": bot_message
        })
        print("YouTube Bot:", textwrap.fill(bot_message, 60), "\n")
        return

    def freed_chatbot(self):
        new_topic_prompt = False
        self.message_log.append({
            "role": "system",
            "content": "Continue the conversation about the topic above!"})
        while True:
            user_msg = input("{}: ".format(self.user_name))
            print()
            if user_msg == '!exit':
                print("Thanks for talking to Youtube Bot :)\n")
                sys.exit(0)
            if user_msg == "!newtopic":
                self.ask_user_thoughts()
                return
            self.message_log.append({"role": "user", "content": user_msg})
            bot_message = self.chat.generate_message(self.message_log)
            self.message_log.append({"role": "assistant", "content": bot_message})
            print("YouTube Bot:", textwrap.fill(bot_message, 60))
            if not new_topic_prompt:
                print("Youtube Bot: **If you want to change the topic, just say `!newtopic`**\n")
                new_topic_prompt = True

    def ask_user_thoughts(self):
        bot_message = self.chat.generate_thoughts(self.user_data.previous_msg_list)
        print("YouTube Bot: ", bot_message, "\n")
        self.user_data.add_previous_msg_list(bot_message)
        user_thoughts = input("{}: ".format(self.user_name))
        print()
        if user_thoughts == '!exit':
            print("Thanks for talking to Youtube Bot :)\n")
            sys.exit(0)
        self.user_data.add_thoughts(user_thoughts)
        print("Youtube Bot: Thank you for the insight!\n")
        with open('chat_data.p', 'wb') as f:
            pickle.dump(self.user_data, f)
        return

    def regular_chat(self):
        self.message_log.append(
            {"role": "system", "content": "Generate your first response, given the information above."})
        self.message_log.append({
            "role": "system",
            "content": "After the user responds, continue the conversaion how ChatGPT normally would"})
        bot_message = self.chat.generate_message(self.message_log)
        while True:
            print("YouTube Bot:", textwrap.fill(bot_message, 60), "\n")
            user_msg = input("{}: ".format(self.user_name))
            print()
            if user_msg == '!exit':
                print("Thanks for talking to Youtube Bot :)\n")
                sys.exit(0)
            self.message_log.append({"role": "user", "content": user_msg})
            bot_message = self.chat.generate_message(self.message_log)


if __name__ == '__main__':
    main = Main()
    main.main_chat()
