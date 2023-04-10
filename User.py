class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []
        self.previous_msg_list = []
        self.thoughts = []
        
    def add_previous_msg_list(self, msg):
        self.previous_msg_list.append(msg)
        
    def add_thoughts(self, thoughts):
        self.thoughts.append(thoughts)