   
from collections import defaultdict
from datetime import datetime, timedelta
from random import randint
from re import search
from time import time

from . import db
from .cmds import games

welcomed = []
messages = defaultdict(int)
messagesText = defaultdict()


def process(bot, user, message):
    update_records(bot, user)

    if user["id"] not in welcomed:
        welcome(bot, user)
    
    elif "bye" in message:
        say_goodbye(bot, user)
    
    #if user["id"] != ""
    check_activity(bot, user)

    if (match := search(r'cheer[0-9]+', message)) is not None:
        thank_for_cheer(bot, user, match)
        
    if (h := games.heist) is not None:
        if h.start_time <= time() and not h.running:
            games.run_heist(bot)
        
        elif h.end_time <= time() and h.running:
            games.end_heist(bot)


def update_records(bot, user):
    db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)",
    user["id"])

    db.execute("UPDATE users SET MessagesSent = MessagesSent + 1 WHERE UserID = ?",
        user["id"])

    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?",
        user["id"])

    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")

        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?",
            randint(1,5), coinlock, user["id"])

def welcome(bot, user):
    bot.send_message(f"KonCha Welcome to the poo show {user['name']}!")
    welcomed.append(user["id"])


def say_goodbye(bot, user):
    bot.send_message(f"See ya later {user['name']} HungryPaimon !")
    welcomed.remove(user["id"])


def check_activity(bot, user):
    messages[user["id"]] += 1
    if (count := messages[user["id"]]) == 150:
        bot.send_message(f"Poggers {user['name']} - you've sent {count:,} messages! TehePelo")
    elif (count := messages[user["id"]]) == 75:
        bot.send_message(f"AWWW Shiz {user['name']} - you've sent {count:,} messages! TehePelo")
    elif (count := messages[user["id"]]) == 50:
        bot.send_message(f"Indeed Indeed {user['name']} - you've sent {count:,} messages! TehePelo")
    elif (count := messages[user["id"]]) == 25:
        bot.send_message(f"MmmHmmm {user['name']} - you've sent {count:,} messages! TehePelo")   
    else:
        if (count := messages[user["id"]]) == 3:
            bot.send_message(f"Thanks for being active in chat {user['name']} - you've sent {count:,} messages! TehePelo")


def thank_for_cheer(bot, user, match):
    bot.send_message(f"Thank your for the {int(match.group()[5:]):,} bitties to see my Kitty (.)(.)'s {user['name']}! ")