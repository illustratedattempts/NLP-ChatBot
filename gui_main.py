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

message("test")

# @TODO Will need to work on getting the input box to be at the bottom
if 'state' not in st.session_state:
    st.session_state['state'] = ['New_Instance']
    st.session_state['checked_history'] = None
    st.session_state['prev_user_log'] = None
    st.session_state['user_name'] = None
    st.session_state['topic_input'] = None
    st.session_state['video_title'] = None
    st.session_state['video_link'] = None
    st.session_state['videos_link_arr'] = []
    st.session_state['videos_title_arr'] = []
    st.session_state['message_logs'] = []
    yt = st.session_state[
        'YT_OBJ'] = YoutubeToolkit()  # Error Here Perhaps? (file_cache is only supported with oauth2client<4.0.0)
    # st.session_state['NLP_OBJ'] = NLPTechniques()


# message("State before switch-case: " + str(st.session_state['state'][-1]))


# An observation is that the st.session_state is saved somehow regardless of continuous reruns of the invoked python file
# This implies that when a program is rerun, the memory is not saved yet this is a contradiction to that reasoning.

# This is for a new run of streamlit, so we have to initialize all the variables here

def check_if_history_exists():
    files_list = os.listdir('./')
    for file in files_list:
        if file.endswith('.p'):
            st.session_state['prev_user_log'] = file
            return True
    return False


def get_text():
    # https://stackoverflow.com/questions/2603956/can-we-have-assignment-in-a-condition
    # https://discuss.streamlit.io/t/how-to-hide-streamlit-text-input-after-input/10832/2
    text_input_container = st.empty()
    text = text_input_container.text_input("STUFF: ", key='input')
    if not text:  # When the text is empty
        st.stop()
        message("Here!")  # st.stop()  # Stop pauses the code execution at this point
    else:
        del st.session_state['input']
        text_input_container.empty()
        message(text, is_user=True)
    return text


match st.session_state['state'][-1]:
    case 'New_Instance':
        if not check_if_history_exists():
            message("What's your name?")
            name_input = get_text()
        else:  # User data already exists in the directory
            print("@TODO Implement Importing User Data")
        st.session_state['state'].append('Start_New_Topic')
        message("New_Instance")

    case 'Start_New_Topic':
        message("What do you want to discuss?")
        st.session_state['state'].append('Take_Topic_Input')

    case 'Take_Topic_Input':
        st.session_state['topic_input'] = get_text()
        if re.search("youtu.be\/|youtube.com\/|https", st.session_state['topic_input']):
            st.session_state['state'].append('Topic_Is_Link')
        else:
            st.session_state['state'].append('Topic_Not_Link')
    case 'Topic_Is_Link':  # Assume that topic_input is not EMPTY
        if yt.verify_url(st.session_state['topic_input']):
            if not yt.verify_comments_enabled(yt.get_video_id(
                    urlparse(st.session_state['topic_input']))):  # Did NOT pass the comments verifier
                message("It seems like the video you've chosen has comment scraping disabled. Please pick another.")
                # We don't need to take in the input as the 'Take_Topic_Input' state already does that
                st.session_state['state'] = 'Take_Topic_Input'  # We go back to the start of the loop
            st.session_state['topic_chosen'] = st.session_state['topic_input']
        else:
            message("Whoops YOUR URL does not seem to work. Please try again.")
            message("Please ensure the link does not contain timestamps or anything after the Video ID.")
            st.session_state['state'].append('Take_Topic_Input')
    case 'Topic_Not_Link':  # We automatically assume its a topic
        st.session_state['videos_link_arr'], st.session_state['videos_title_arr'] = yt.get_topic_list(
            st.session_state['topic_input'])
        videos_link_arr = st.session_state['videos_link_arr']
        videos_title_arr = st.session_state['videos_title_arr']
        videos_list = ''
        for num in range(len(st.session_state['videos_link_arr'])):
            videos_list += str(num + 1) + '. ' + html.unescape(videos_title_arr[num]) + ' | ' + videos_link_arr[
                num] + '\n'
        message(videos_list)
        st.session_state['state'].append('Choose_Video_Number')
message("I'm out!")
st.write(st.session_state)
st.experimental_rerun()
