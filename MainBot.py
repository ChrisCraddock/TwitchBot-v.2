"""
	COPYRIGHT INFORMATION
	---------------------
Python Twitch bot (MainBot.py)
	Copyright © Parafoxia 2020.
	Copyright © Carberra 2020.
    Copyright © FuzzybuttGames 2020.
This bot was created on the Carberra YouTube channel. The tutorial series it featured in can be found here:
	https://www.youtube.com/playlist?list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO
This bot can be freely copied and modified without permission, but not sold as is.
Some code in this file is licensed under the Apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/
	NOTES
	-----
You will obviously need to modify `NAME`, `OWNER`, `bot.CLIENT_ID`, and `bot.TOKEN` to your own info before running the bot.
Otherwise, the modifications to this code, and all the code in the /lib directory, are copyright © FuzzybuttGames 2020.
"""
from twitchAPI.twitch import Twitch
from irc.bot import SingleServerIRCBot
from requests import get
import NO_SHARE 

from lib import db, cmds, react #logs

NAME = NO_SHARE.BOT_NAME #My bots name 
OWNER = NO_SHARE.CHNL_NAME #My gaming channel name
twitch = Twitch(NO_SHARE.APP_ID, NO_SHARE.APP_SCRT) #app_id app_secret

class Bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = NO_SHARE.BOT_ID #My bots ID
        self.TOKEN = NO_SHARE.BOT_TOKEN #My bots Token
        self.CHANNEL = f"#{OWNER}"

        user_info = twitch.get_users(logins=['fuzziestfuzzy'])
        user_id = user_info['data'][0]['id']

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")
        
        cxn.join(self.CHANNEL)
        db.build()
        self.send_message("Now Online.")

    @db.with_commit
    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        if user["name"] != NAME:
            react.process(bot, user, message)
            cmds.process(bot, user, message)

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)


if __name__=="__main__":
    bot = Bot()
    bot.start()