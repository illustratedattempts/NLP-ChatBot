import os
import openai
from dotenv import load_dotenv

class Chatbot:
    def __init__(self):
        # Get API key from environment variable
        load_dotenv("api_keys.env")
        openai.api_key = os.getenv("OPENAI_KEY")
        
    def send_system_message(self, sys_msg):
        message = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": sys_msg},
                ],
            max_tokens = 1024
        )
    
    def generate_message(self, user_msg):
        message = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a pirate. Act like it."},
                {"role": "user", "content": user_msg}
                ],
            max_tokens = 1024
        )
        return message.choices[0].message.content
