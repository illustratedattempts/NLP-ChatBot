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
import streamlit as st
from streamlit_chat import message

def check_if_history_exists():
    files_list = os.listdir('./')
    for file in files_list:
        if file.endswith('.p'):
            st.session_state['prev_user_log'] = file
            return True
    return False


def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 

def get_likes_and_dislikes():
    st.session_state['generated'].append("What do you like about the video?")
    text = get_text("User")
    if text == '!newtopic':
        st.session_state['state'] = 'Ask_Feedback'
    if text == '!exit':
        st.session_state['generated'].append("Thanks for trying Youtube Bot! :)")
        sys.exit(0)
    st.session_state['user'].likes.append(text)
    st.session_state['past'].append(text)
    with open('chat_data.p', 'wb') as f:
        pickle.dump(st.session_state['user'], f)
    st.session_state['generated'].append("What do you not like about the video?")
    text = get_text("User")
    if text == '!newtopic':
        st.session_state['state'] = 'Ask_Feedback'
    if text == '!exit':
        st.session_state['generated'].append("Thanks for trying Youtube Bot! :)")
        sys.exit(0)
    st.session_state['user'].dislikes.append(text)
    st.session_state['past'].append(text)
    with open('chat_data.p', 'wb') as f:
        pickle.dump(st.session_state['user'], f)

def chatbot_configs():
    # Get the comments from the video
    comments = st.session_state['YT_OBJ'].comment_finder(
        st.session_state['link']
    )
    # clean_comments type list
    clean_comments = st.session_state['NLP_OBJ'].clean_text_array(comments)
    comment_freq = st.session_state['NLP_OBJ'].word_frequency(clean_comments)

    # Setup chatbot to discuss current video
    # Give the chatbot the title of the video
    st.session_state['message_log'].append(
        {"role": "system", "content": "You are a bot that pretends to give analysis on Youtube videos."})
    st.session_state['message_log'].append({"role": "system",
                                "content": "You do not need to have knowledge on the videos, just give an analysis based on sentiment score and title."})
    st.session_state['message_log'].append({"role": "system",
                                "content": "Also, try to utilize keywords that relate to the video in your response."})
    title_message = "The video you are currently discussing is called " + st.session_state['YT_OBJ'].get_video_name(link)
    st.session_state['message_log'].append({"role": "system", "content": title_message})
    
    # Give the user feedback on the video
    user_likes = "The user likes this about the video " + st.session_state['user'].likes[-1]
    user_dislikes = "The user does not like this about the video " + st.session_state['user'].dislikes[-1]
    st.session_state['message_log'].append(
        {"role": "system", "content": user_likes})
    st.session_state['message_log'].append(
        {"role": "system", "content": user_dislikes})

    # Give the chatbot the sentiment analysis of the comments
    sentiment_score = st.session_state['NLP_OBJ'].sentiment_analysis(" ".join(comments))
    sentiment_message = "The video you are currently discussing has a sentiment score of " + str(
        sentiment_score[0]) + " percent negative, " + str(sentiment_score[1]) + " percent neutral, and " + str(
        sentiment_score[2]) + " percent positive."
    st.session_state['message_log'].append({"role": "system", "content": sentiment_message})

    # Give the chatbot the most frequent words in order
    common_words = []
    for key, value in sorted(comment_freq.items(), key=lambda x: x[1], reverse=True):
        common_words.append(key)

    # Send the bot the 100 most common words
    common_words_message = "The most common words commented under the video are "
    for i in range(0, min(len(common_words), 100)):
        common_words_message += common_words[i] + " "
    st.session_state['message_log'].append({"role": "system", "content": common_words_message})
    st.session_state['message_log'].append(
        {"role": "system", "content": "Generate your first response, given the information above."})
    bot_message = st.session_state["CT_OBJ"].generate_message(st.session_state['message_log'])
    st.session_state['message_log'].append({
        "role": "assistant",
        "content": bot_message
    })
    st.session_state['generated'].append(bot_message)

def ask_feedback():
    bot_message = st.session_state["CT_OBJ"].generate_thoughts(
        st.session_state['user'].previous_msg_list
    )
    st.session_state['generated'].append(bot_message)
    text = get_text("User")
    if text == '!newtopic':
        st.session_state['state'] = 'Ask_Feedback'
    if text == '!exit':
        st.session_state['generated'].append("Thanks for trying Youtube Bot! :)")
        sys.exit(0)
    st.session_state['user'].thoughts.append(text)
    st.session_state['past'].append(text)
    with open('chat_data.p', 'wb') as f:
        pickle.dump(st.session_state['user'], f)
    st.session_state['state'] = 'Start_New_Topic'


def freed_chat():
    st.session_state['message_log'].append({
        "role": "system",
        "content": "Continue the conversation about the topic above!"})
    st.session_state['generated'].append("If you want a new topic, feel free to use !newtopic")
    while True:
        text = get_text("User")
        if text == '!newtopic':
            st.session_state['state'] = 'Ask_Feedback'
        if text == '!exit':
            st.session_state['generated'].append("Thanks for trying Youtube Bot! :)")
            sys.exit(0)
        st.session_state['past'].append(text)
        st.session_state['message_log'].append({"role": "user", "content": text})
        bot_message = st.session_state["CT_OBJ"].generate_message(
            st.session_state['message_log']
        )
        st.session_state['message_log'].append({"role": "assistant", "content": bot_message})
        st.session_state['generated'].append(bot_message)
    
"""
if 'state' not in st.session_state:
    st.session_state['state'] = ['New_Instance']
    st.session_state['checked_history'] = None
    st.session_state['prev_user_log'] = None
    st.session_state['user'] = None
    st.session_state['message_history'] = None
    st.session_state['CB_OBJ'] = Chatbot()
    st.session_state['YT_OBJ'] = YoutubeToolkit() # Error Here Perhaps? (file_cache is only supported with oauth2client<4.0.0)
    st.session_state['NLP_OBJ'] = NLPTechniques()
"""
if "state" not in st.session_state:
    st.session_state['state'] = 'Freed_Chat'
    st.session_state['message_log'] = []
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['CB_OBJ'] = Chatbot()

match st.session_state['state'][-1]:
    case 'New_Instance':
        if not check_if_history_exists():
            st.session_state['generated'].append("What's your name?")
            user_input = get_text('User')
            st.session_state['user'] = User(user_input)
            with open('chat_data.p', 'wb') as f:
                pickle.dump(st.session_state['user'], f)
        else:  # User data already exists in the directory
            print("@TODO Implement Importing User Data")
            st.session_state['user'] = st.session_state['prev_user_log']
            st.session_state['prev_user_log'] = None
        st.session_state['generated'].append("Hello " + st.session_state['user'].name)
        st.session_state['generated'].append("Whenever you want to leave the chat, use !exit")
        st.session_state['state'].append('Start_New_Topic')
    case 'Start_New_Topic':
        st.session_state['generated'].append('What do you want to discuss?')
    case 'Get_Likes_And_Dislikes':
        get_likes_and_dislikes()
    case 'Chatbot_Configs':
        chatbot_configs()
    case 'Freed_Chat':
        freed_chat()
    case 'Add_Feedback':
        ask_feedback()

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

