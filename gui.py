import streamlit as st
from streamlit_chat import message
from chatbot.Chatbot import Chatbot

# - If no chat history exists, prompt Chatbot to ask user about their likes and dislikes
# - Make chat history a downloadable object

# Create title for the page
st.title("HLT Chatbot demo")

# Create the header and markdown (below header)
st.header("HLT Chatbot")
st.markdown("Alejo Vinluan (abv210001)\nThanh Vo (netid)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
    
def get_message():
    text_input = st.text_input("Message: ","")
    return text_input

chat = Chatbot()

user_msg = get_message()

if 'prompt' not in st.session_state:
    initial_msg = "Send a YouTube link about the video you want to talk about"
    message(initial_msg)
    message(user_msg, is_user=True)

if user_msg:
    st.session_state['prompt'] = True
    response = chat.generate_message(user_msg)
    st.session_state.past.append(user_msg)
    st.session_state.generated.append(response)

if st.session_state['prompt']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')