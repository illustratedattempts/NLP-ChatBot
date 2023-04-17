import streamlit as st
from streamlit_chat import message
import sys
import random
import re

# Check if this is a NEW run
if 'state' not in st.session_state:
    st.session_state['state'] = ['New_Instance']
    st.session_state['message_logs'] = ['Testing']
    st.session_state['name_prompt'] = False
    st.session_state['user'] = None
    st.session_state['enter_prompt'] = False
    st.session_state['testing_topic'] = None
    st.session_state['comment_not_enabled_prompt'] = False


def generate_random_key():
    return random.randint(-sys.maxsize, sys.maxsize)


# Print out ALL message logs on RERUN
for item in st.session_state['message_logs']:
    if '78910689:' in item:
        message(item[9:], is_user=True, key=generate_random_key())
    elif '3979773:' in item:
        message(item[8:], key=generate_random_key())
    else:
        message("SYSTEM: " + item, key=generate_random_key())


# 78910689: represents the user
# 3979773: represents the system
def user_text():
    container = st.empty()
    input_text = container.text_input("ENTER STUFF HERE:")
    if not input_text:
        st.stop()  # We want the execution of code to stop here
    else:  # Streamlit does refresh on ENTER of text input
        # Somehow it realizes that there's something in the place where input_text should be (in memory?) after rerun and then executes the else statement
        # Probably because it goes back to the container and sees that it still exists??? NVM
        st.session_state['message_logs'].append('78910689:' + input_text)  # Stores the user message to be displayed
        container.empty()  # No point in putting in a message function call as at this point the code will just be rerun
        return input_text


def display_robot_msg(text):
    st.session_state['message_logs'].append("3979773:" + text)
    message(text, key=generate_random_key())


# There's a lot of delicacy between choosing which message to display at the moment and on refresh
# For STATES that have user_input prompts, you need to have a switch so that it gets appended once to message logs
match st.session_state['state'][-1]:
    case 'New_Instance':
        if False:  # @TODO check_if_history_exists() Will Go Here
            if not st.session_state['name_prompt']:  # Only DOES this ONCE
                display_robot_msg("What's your name?")
                st.session_state['name_prompt'] = True
                user_text()
            st.session_state['name_prompt'] = False  # Re-flips the switch for later use?
        else:  # We assume that the user profile exists here
            st.session_state['user'] = "User Person"  # TODO Get the username somehow
            display_robot_msg("Hello, " + st.session_state['user'])
            # display_robot_msg("Whenever you want to leave the chat, use !exit")  # @TODO IMPLEMENT LATER?

        st.session_state['state'].append('Start_New_Topic')
        st.experimental_rerun()
    case 'Start_New_Topic':
        display_robot_msg("What do you want to discuss?")

        st.session_state['state'].append('Topic_Selection')
        st.experimental_rerun()
    case 'Topic_Selection':
        if not st.session_state['enter_prompt']:
            display_robot_msg("Please enter JUST the topic or link.")
            st.session_state['enter_prompt'] = True

        st.session_state[
            'testing_topic'] = user_text()  # Interesting interaction, if you have this line inside the if statement it will not do the assignment operation
        st.session_state['enter_prompt'] = False

        st.session_state['state'].append('Link_OR_Topic')
        st.experimental_rerun()
    case 'Link_OR_Topic':
        if re.search("youtu.be\/|youtube.com\/|https", st.session_state['testing_topic']):
            st.session_state['state'].append('Link_Provided')
            st.experimental_rerun()
        else:
            st.session_state['state'].append('Topic_Provided')
            st.experimental_rerun()
    case 'Link_Provided':
        if re.search(
                '(https:\/\/)?(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9\-\_]{11}$|(https:\/\/)?(www\.)?youtu\.be\/[a-zA-Z0-9\-\_]{11}',
                st.session_state['testing_topic']):
            if not False:  # @TODO Implement to see if comments enabled
                if not st.session_state['comment_not_enabled_prompt']:
                    display_robot_msg(
                        "It seems like the video you have chosen has comment scraping disabled. Please pick another.")
                    st.session_state['comment_not_enabled_prompt'] = True

                st.session_state['testing_topic'] = user_text()
                st.session_state['comment_not_enabled_prompt'] = False

                st.session_state['state'].append('Link_OR_Topic')
                st.experimental_rerun()
            else:
                st.session_state['state'].append('Topic_Chosen')
                st.experimental_rerun()
    case 'Topic_Provided':
        display_robot_msg("Please Pick a Video From The Following Listed Below")

    # @TODO Checking the inputs etc etc

    case 'Topic_Chosen':
        print("THIS NEVER RUNS! GOTTA DELETE LATER!")

