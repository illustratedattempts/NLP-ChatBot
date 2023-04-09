import sys
from chatbot.Chatbot import Chatbot
from chatbot.YoutubeToolkit import YoutubeToolkit
from chatbot.NLPTechniques import NLPTechniques
import os
import pickle
import re


class Main:
    def __init__(self):
        self.prev_user_log = None
        self.chat = Chatbot()
        self.yt = YoutubeToolkit()
        self.nlp = NLPTechniques()
        self.user_name = ""
        self.message_log = []

    def check_if_first_instance(self):
        files_list = os.listdir('./')  # Get List of Files/Directories in Directory | Can be changed to look at
        # different places [LATER]
        pickle_file_exists = False
        for file in files_list:
            if '.p' in file:  # Check if any file has the .p extension
                self.prev_user_log = file
                pickle_file_exist = True
                break

        return pickle_file_exist

    def main_chat(self):
        # We check if this is a new chat instance
        if self.check_if_first_instance():
            print("Youtube Bot: What's your name?")
            self.user_name = input("User: ")
            print("Youtube Bot: Hello ", self.user_name, "!", sep='')
        else:  # User Data already exists in the directory
            if self.prev_user_log is None:
                print("ERROR!")
                return
            else:
                user_data = pickle.load(open(self.prev_user_log), 'rb')
                self.user_name = "Something Here :>"  # Need to unpack the user_data username properly
                print("Youtube Bot: Hello, " + self.user_name)
        self.looping_functionality()

    def looping_functionality(self):
        while True:
            print("Youtube Bot: What do you want to discuss?")  # Could have variational ways of saying the same thing

            # Keeps GOING until video is verified
            while True:
                video_link, video_title = self.topic_verification()  # Will ALWAYS be FORCED to return THIS UNLESS
                print("Youtube Bot: ARE YOU SURE THIS IS THE VIDEO YOU WANT TO DISCUSS?(Y/N) {}".format(video_title))
                confirmation_input = input()  # @TODO Need to make it all either caps or lower case
                if confirmation_input == 'Y':
                    break

            # Prompt to store LIKES/DISLIKES
            print("Youtube Bot: What do you like about {}?".format(video_title))
            user_likes = input()
            print("Youtube Bot: Okay.")
            print("Youtube Bot: What do you dislike about {}?".format(video_title))
            user_dislikes = input()
            # @TODO Store user likes/dislikes somehow
            # exiting the ENTIRE PROGRAM after this

    def topic_verification(self):
        """
        The user either enters a URL or topic. If it is not a working URL then we force them to enter a URL or topic.
        Otherwise, we immediately assume it's a topic.
        """
        print("Youtube Bot: Please enter JUST the topic or link.")
        user_input = input()
        while True:
            if re.search("youtu.be\/|youtube.com\/|https", user_input):  # Check if the user's input has a link
                if self.yt.verify_url(user_input):  # Verify the URL works
                    return user_input, self.yt.get_video_name(user_input)
                else:
                    print("Youtube Bot: WHOOPS. Your URL does not seem to work. Please try again or enter a topic.")
            else:  # VIDEO SEARCH FROM TOPIC
                videos_link_arr, videos_title_arr = self.yt.get_topic_list(user_input)

                print("Please Pick a Video From The Following:")
                for num in range(len(videos_title_arr)):
                    print(str(num + 1) + '. ' + videos_title_arr[num])
                print("Enter the Number: ", end='')
                selected_vid_index = int(input())  # ASSUMES that the result is the index
                selected_vid_index = selected_vid_index - 1
                return videos_link_arr[selected_vid_index], videos_title_arr[selected_vid_index]

            # We KNOW that the URL is not correct or THEY chose to enter a topic instead
            user_input = input()

    def start_chat(self):
        print("YouTube Bot: Hello! I am YouTube bot.")
        print("YouTube Bot: What's your name?\n")
        self.user_name = input("User: ")
        print("\nYouTube Bot: Hello ", self.user_name, "!", sep='')
        print("YouTube Bot: What do you want to discuss? Feel free to send a link or topic.\n")
        discussion = input("{}: ".format(self.user_name))
        
        # If user's next message is a URL
        #  (we are currently assuming YouTube URL is sent)
        if self.yt.verify_url(discussion):
            # Get the comments from the video
            comments = self.yt.comment_finder(discussion)
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
            title_message = "The video you are currently discussing is called " + self.yt.get_video_name(discussion)
            self.message_log.append({"role": "system", "content": title_message})

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
            self.regular_chat()
        else:  # TOPIC SEARCH
            videos_id_arr, videos_title_arr = self.yt.get_topic_list(discussion)

            print("Please Pick a Video From The Following:")
            for num in range(len(videos_title_arr)):
                print(str(num + 1) + '. ' + videos_title_arr[num])
            print("Enter the Number: ", end='')
            selected_vid_index = int(input())  # ASSUMES that the result is the index
            selected_vid_index = selected_vid_index - 1

            video_link = "https://www.youtube.com/watch?v=" + videos_id_arr[selected_vid_index]

    def regular_chat(self):
        self.message_log.append(
            {"role": "system", "content": "Generate your first response, given the information above."})
        bot_message = self.chat.generate_message(self.message_log)
        while (True):
            print("\nYouTube Bot:", bot_message, "\n")
            user_msg = input("{}: ".format(self.user_name))
            self.message_log.append({"role": "user", "content": user_msg})
            bot_message = self.chat.generate_message(self.message_log)


if __name__ == '__main__':
    main = Main()
    # Check if history file is provided
    """
    if len(sys.argv) == 2:
        main.load_history()
    else:
        main.start_chat()
    """
    main.check_if_first()
