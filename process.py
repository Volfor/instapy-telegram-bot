import multiprocessing, datetime, json, time, os, sys

# Colored terminal
from termcolor import colored, cprint

class Process (multiprocessing.Process):
    def __init__(self, instapy_path, script_name, chat_id, bot, username, password, scripts, proxy=None):
        multiprocessing.Process.__init__(self)
        self.instapy_path = instapy_path
        self.script_name = script_name
        self.chat_id = chat_id
        self.bot = bot
        self.username = username
        self.password = password
        self.scripts = scripts
        self.proxy = proxy
        
    def return_attribute(self):
        return {
            "instapy_path": self.instapy_path,
            "script_name": self.script_name,
            "scripts": self.scripts,
            "chat_id": self.chat_id ,
            "bot": self.bot,
            "user": {
                "username": self.username,
                "password": self.password,
                "proxy": self.proxy
            }
        }

    # self.bot.send_message does not work if called by the parent.
    def end(self, forced=True):
        if forced is True:
            self.terminate()
        
        end = datetime.datetime.now().replace(microsecond=0)
        self.bot.send_message(self.chat_id, text='InstaPy Bot end at {}\nExecution time {}'.format(time.strftime("%X"), end-self.start))
        
    def run(self):
        sys.path.append(self.instapy_path)  
        from instapy import InstaPy      

        self.start = datetime.datetime.now().replace(microsecond=0)
        self.bot.send_message(self.chat_id, text='InstaPy Bot - {} start at {}'.format(self.script_name, time.strftime("%X")))
        
        self.scripts[self.script_name](InstaPy, self.username, self.password, self.proxy)

        self.end(forced=False)
