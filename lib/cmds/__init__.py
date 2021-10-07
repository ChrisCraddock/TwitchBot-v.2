from time import time

from . import misc, economy, games



PREFIX = "!"


class Cmd(object):
    def __init__(self, callables, func, cooldown=0):
        self.callables = callables
        self.func = func
        self.cooldown = cooldown
        self.next_use = time()

#cmds = {
#    "hello": misc.hello,
#}


cmds = [
    # misc
    Cmd(["hello", "hi", "hey"], misc.hello, cooldown=10),
    Cmd(["about"], misc.about, cooldown=10),
    Cmd(["uptime"], misc.uptime, cooldown=10),
    Cmd(["userinfo", "ui"], misc.userinfo, cooldown=10),
    Cmd(["shutdown"], misc.shutdown),

    
    # economy
    Cmd(["coins", "money"], economy.coins),

    # games
    Cmd(["coinflip", "flip"], games.coinflip, cooldown=6),
    Cmd(["heist"], games.start_heist, cooldown=60),

    #WebSocket
    #Cmd(["currentName"], WSEvents.currentName, cooldown=60)
]


def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)


def perform(bot, user, call, *args):
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
    
    else:
        for cmd in cmds:
            if call in cmd.callables:
                if time() > cmd.next_use:
                    cmd.func(bot, user, *args)
                    cmd.next_use = time() + cmd.cooldown
                
                else:
                    bot.send_message(f"FootYellow Cooldown still in effect.  Try again in {cmd.next_use-time():,.0f} seconds.")
                
                return

        bot.send_message(f"{user['name']}, \"{call}\" has not been learnted yet (but I'm sure Streamlabs will take care of it if it knows).")
