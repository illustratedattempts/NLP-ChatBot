import os
import openai
from dotenv import load_dotenv

class Chatbot:
    def __init__(self):
        # Get API key from environment variable
        load_dotenv("api_keys.env")
        openai.api_key = os.getenv("OPENAI_KEY")
        
    def generate_message(self, msg_log):
        message = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = msg_log,
            max_tokens = 1024
        )
        return message.choices[0].message.content

    def generate_thoughts(self, previous_asked):
        message = openai.Completion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system",
                 "content" : "Create a message asking `What did you think about our conversation?`"},
                {"role": "system",
                 "content": "Avoid using the ways you've previously asked before: "},
                {"role": "system",
                 "content": " ".join(previous_asked)}
            ]
        )
        return message.choices[0].message.content