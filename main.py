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
topic_selected = False

if 'prompt' not in st.session_state:
    initial_msg = "Pick a topic to talk about (i.e. Backpacking in Europe, Meal prep recipes, etc.)"
    message(initial_msg)
    message(user_msg, is_user=True)
    # We assume the user actually types in a topic
    #  If we have extra time, we can do verification.
    #  (i.e. user types in 1 letter or 1 number only, nonsense, empty string, etc.)
    
    
    
if user_msg and topic_selected:
    st.session_state['prompt'] = True
    response = chat.generate_message(user_msg)
    st.session_state.past.append(user_msg)
    st.session_state.generated.append(response)

if st.session_state['prompt']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')