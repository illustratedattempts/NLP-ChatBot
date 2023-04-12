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


# @TODO Will need to work on getting the input box to be at the bottom
#
def main():
    # An observation is that the st.session_state is saved somehow regardless of continuous reruns of the invoked python file
    # This implies that when a program is rerun, the memory is not saved yet this is a contradiction to that reasoning.

    # This is for a new run of streamlit, so we have to initialize all the variables here
    if 'state' not in st.session_state:
        st.session_state['state'] = ['New_Instance']
        st.session_state['checked_history'] = None
        st.session_state['prev_user_log'] = None
        st.session_state['user_name'] = None
        # st.session_state['YT_OBJ'] = YoutubeToolkit() # Error Here Perhaps? (file_cache is only supported with oauth2client<4.0.0)
        # st.session_state['NLP_OBJ'] = NLPTechniques()
    # message("State before switch-case: " + str(st.session_state['state'][-1]))

    match st.session_state['state'][-1]:
        case 'New_Instance':
            if not check_if_history_exists():
                message("What's your name?")
                user_input = get_text('User')
                message("Dumpster Fire!")
            else:  # User data already exists in the directory
                print("@TODO Implement Importing User Data")
            st.session_state['state'].append('Start_New_Topic')
        case 'Start_New_Topic':
            message('What do you want to discuss?')


def check_if_history_exists():
    files_list = os.listdir('./')
    for file in files_list:
        if file.endswith('.p'):
            st.session_state['prev_user_log'] = file
            return True
    return False


def get_text(user_name):
    # https://stackoverflow.com/questions/2603956/can-we-have-assignment-in-a-condition
    # https://discuss.streamlit.io/t/how-to-hide-streamlit-text-input-after-input/10832/2
    text_input_container = st.empty()
    text = text_input_container.text_input("User")

    if not text:
        st.stop()
    else:
        text_input_container.empty()
        st.info(text)
    return text

if __name__ == '__main__':
    main()
