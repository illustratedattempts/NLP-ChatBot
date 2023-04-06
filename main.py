import streamlit as st
from streamlit_chat import message
from chatbot.Chatbot import Chatbot

# Create title for the page
st.set_page_config(
    page_title="HLT Chatbot"
)

# Create the header and markdown (below header)
st.header("HLT Chatbot")
st.markdown("Alejo Vinluan (abv210001)\nThanh Vo (ttv170230)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


def get_message():
    text_input = st.text_input("Message: ", "")
    return text_input


chat = Chatbot()
user_msg = get_message()

if user_msg:
    response = chat.generate_message(user_msg)
    st.session_state.past.append(user_msg)
    st.session_state.generated.append(response)

st.write(st.session_state)
