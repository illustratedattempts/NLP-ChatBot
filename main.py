import sys
from chatbot.Chatbot import Chatbot
from chatbot.YoutubeToolkit import YoutubeToolkit
from chatbot.NLPTechniques import NLPTechniques

class Main:
    def __init__(self):
        self.chat = Chatbot()
        self.yt = YoutubeToolkit()
        self.nlp = NLPTechniques()
        self.user_name = ""
        self.message_log = []
    
    def start_chat(self):
        print("YouTube Bot: Hello! I am YouTube bot.")
        print("YouTube Bot: What's your name? ")
        self.user_name = input("User: ")
        print("YouTube Bot: Hello ", self.user_name, "!", sep='')
        print("YouTube Bot: What do you want to discuss? Feel free to send a link or topic. ")
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
            self.message_log.append({"role": "system", "content": "You are a bot that pretends to give analysis on Youtube videos."})
            self.message_log.append({"role": "system", "content": "You do not need to have knowledge on the videos, just give an analysis based on sentiment score and title."})
            self.message_log.append({"role": "system", "content": "Also, try to utilize keywords that relate to the video in your response."})
            title_message = "The video you are currently discussing is called " + self.yt.get_video_name(discussion)
            self.message_log.append({"role": "system", "content": title_message})
            
            # Give the chatbot the sentiment analysis of the comments
            sentiment_score = self.nlp.sentiment_analysis(" ".join(comments))
            sentiment_message = "The video you are currently discussing has a sentiment score of " + str(sentiment_score[0]) + " percent negative, " + str(sentiment_score[1]) + " percent neutral, and " + str(sentiment_score[2]) + " percent positive."
            self.message_log.append({"role": "system", "content": sentiment_message})
            
            # Give the chatbot the most frequent words in order
            common_words = []
            for key, value in sorted(comment_freq.items(), key=lambda x: x[1], reverse=True):
                common_words.append(key)
            
            # Send the bot the 100 most common words
            common_words_message = "The most common words commented under the video are "
            for i in range(0,min(len(common_words),100)):
                common_words_message += common_words[i] + " "
            self.message_log.append({"role": "system", "content": common_words_message})
            self.regular_chat()
            
        
    def regular_chat(self):
        self.message_log.append({"role": "system", "content": "Generate your first response, given the information above."})
        bot_message = self.chat.generate_message(self.message_log)
        while(True):
            print("\nYouTube Bot:", bot_message, "\n")
            user_msg = input("{}: ".format(self.user_name))
            self.message_log.append({"role": "user", "content": user_msg})
            bot_message = self.chat.generate_message(self.message_log)
    
if __name__ == '__main__':
    main = Main()
    # Check if history file is provided
    if len(sys.argv) == 2:
        main.load_history()
    else:
        main.start_chat()