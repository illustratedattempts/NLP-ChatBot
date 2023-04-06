import os
import openai
from dotenv import load_dotenv

class Chatbot:
    def __init__(self):
        # Get API key from environment variable
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_KEY")
        
    def generate_message(self, user_msg):
        message = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a bot that will give your opinions on YouTube videos"},
                #{"role": "system", "content": "Here are example comments that were listed on that video {example_comments}"},
                {"role": "user", "content": user_msg}
                ],
            max_tokens = 1024
        )
        return message.choices[0].message.content