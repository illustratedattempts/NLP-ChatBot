import streamlit as st
from streamlit_chat import message
import sys
import random
import re
import html

from chatbot.YoutubeToolkit import YoutubeToolkit
from urllib.parse import urlparse

# Check if this is a NEW run
if 'state' not in st.session_state:
    st.session_state['state'] = ['New_Instance']
    st.session_state['message_logs'] = ['Testing']
    st.session_state['name_prompt'] = False
    st.session_state['user'] = None
    st.session_state['enter_prompt'] = False
    st.session_state['testing_topic'] = None
    st.session_state['chosen_video_title'] = None
    st.session_state['chosen_video_link'] = None
    st.session_state['comment_not_enabled_prompt'] = False
    st.session_state['verify_prompt'] = False
    st.session_state['Youtube_Obj'] = YoutubeToolkit()



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
        youtube = st.session_state['Youtube_Obj']
        topic = st.session_state['testing_topic']

        if youtube.verify_url(topic):
            if not youtube.verify_comments_enabled(youtube.get_video_id(urlparse(topic))):  # @TODO Implement to see if comments enabled
                if not st.session_state['comment_not_enabled_prompt']:
                    display_robot_msg(
                        "It seems like the video you have chosen has comment scraping disabled. Please pick another.")
                    st.session_state['comment_not_enabled_prompt'] = True

                st.session_state['testing_topic'] = user_text()
                st.session_state['comment_not_enabled_prompt'] = False

                st.session_state['state'].append('Link_OR_Topic')
                st.experimental_rerun()
            else:
                st.session_state['chosen_video_link'] = topic  # Topic is presumed to be a valid link at this point
                st.session_state['chosen_video_title'] = youtube.get_video_name(topic)
                st.session_state['state'].append('Topic_Verification')
                st.experimental_rerun()
    case 'Topic_Provided':
        # Just so I have to write less
        youtube = st.session_state['Youtube_Obj']
        topic = st.session_state['testing_topic']
        videos_link_arr, videos_title_arr = youtube.get_topic_list(topic)

        display_robot_msg("Please Pick a Video From The Following Listed Below")
        videos_list = ''
        for num in range(len(videos_title_arr)):
            videos_list += str(num+1) + '. ' + html.unescape(videos_title_arr[num]) + ' | ' + videos_link_arr[num] + '\n'
        display_robot_msg(videos_list)
        display_robot_msg("Please enter the video integer number.")
        st.session_state['state'].append('Choosing_Topic_Num')
        st.experimental_rerun()
    # @TODO Checking the inputs etc etc
    case 'Choosing_Topic_Num':
        youtube = st.session_state['Youtube_Obj']
        topic = st.session_state['testing_topic']
        videos_link_arr, videos_title_arr = youtube.get_topic_list(topic)

        selected_vid_index = user_text()
        if selected_vid_index.isdigit():
            selected_vid_index = int(selected_vid_index)
            if 0 < selected_vid_index < 6:
                selected_vid_index = selected_vid_index - 1
                if not youtube.verify_comments_enabled(youtube.get_video_id(urlparse(videos_link_arr[selected_vid_index]))):
                    display_robot_msg("It seems like the video you've chosen has comment scraping disabled. Please pick another topic.")
                    st.session_state['state'].append('Topic_Provided')
                    st.experimental_rerun()
                else:
                    st.session_state['chosen_video_link'] = videos_link_arr[selected_vid_index]
                    st.session_state['chosen_video_title'] = videos_title_arr[selected_vid_index]
                    st.session_state['state'].append('Topic_Verification')
                    st.experimental_rerun()
            else:
                display_robot_msg("Please enter a listed video number.")
                st.session_state['state'].append('Topic_Provided')
                st.experimental_rerun()
        else:
            display_robot_msg("Please enter an INTEGER number.")
            st.session_state['state'].append('Topic_Provided')
            st.experimental_rerun()

    case 'Topic_Verification':
        if not st.session_state['verify_prompt']:
            display_robot_msg("Are you sure you want to look at {}? (Y/N)".format(html.unescape(st.session_state['chosen_video_title'])))
            st.session_state['verify_prompt'] = True
        confirm_text = user_text()
        confirm_text = confirm_text.lower()
        st.session_state['verify_prompt'] = False
        if confirm_text == 'y' or confirm_text == 'yes':
            st.session_state['state'].append('Topic_Chosen')
        elif confirm_text == 'n' or confirm_text == 'no':
            display_robot_msg("Alright. Let us try again.")
            st.session_state['state'].append('Topic_Selection')
        else:
            display_robot_msg("Please enter either YES(Y) or NO(N).")
        st.experimental_rerun()

    case 'Topic_Chosen':
        print("WE GOT HERE!!!!")