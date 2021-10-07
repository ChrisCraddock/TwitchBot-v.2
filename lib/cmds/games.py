from random import choice, randint
from time import time

from .. import db

heist = None
heist_lock = time()


def coinflip(bot, user, side=None, *args):
	if side is None:
		bot.send_message("Enter !coinflip followed by either Heads or Tails")

	elif (side := side.lower()) not in (opt := ("h", "t", "heads", "tails")):
		bot.send_message("Enter !coinflip and then one of the following as the side: " + ", ".join(opt))

	else:
		result = choice(("heads", "tails"))

		if side[0] == result[0]:
			db.execute("UPDATE users SET Coins = Coins + 25 WHERE UserID = ?",
				user["id"])
			bot.send_message(f"It landed on {result}! You won 25 coins!")

		else:
			bot.send_message(f"It landed on {result}! BibleThump Better luck next time...maybe?")


class Heist(object):
	def __init__(self):
		self.users = []
		self.running = False
		self.start_time = time() + 10
		self.end_time = 0
		self.messages = {
			"success" : [
				"{} fought off the guards, and got their haul!",
				"{} sneaked out of the back entrance with their share!",
				"{} got in and out seemlessly with their money!",
			],
			"fail" : [
				"{} got caught by the guards!",
				"{} was turned into a hooker.",
				"{} got lost!",
			]
		}

	def add_user(self, bot, user, bet):
		if self.running:
			bot.send_message("SabaPing You gotta be quicker than that! You'll have to wait until the next one.")

		elif user in self.users:
			bot.send_message("You're already in the group.")

		elif bet > (coins := db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])):
			bot.send_message(f"You don't have that much to bet - you only have {coins:,} coins.")

		else:
			db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
				bet, user["id"])
			self.users.append((user, bet))
			bot.send_message("This is a bold move, lets see if it pays off...")

	def start(self, bot):
		bot.send_message("Standby for results...")
		self.running = True
		self.end_time = time() + randint(1, 2)

	def end(self, bot):
		succeeded = []

		for user, bet in self.users:
			if randint(0, 1):
				db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
					bet*4.5, user["id"])
				succeeded.append((user, bet*4.5))
				bot.send_message(choice(self.messages["success"]).format(user["name"]))

			else:
				bot.send_message(choice(self.messages["fail"]).format(user["name"]))

		if len(succeeded) > 0:
			bot.send_message("The heist is over! The winners: "
				+ ", ".join([f"{user['name']} ({coins:,} coins)" for user, coins in succeeded]))

		else:
			bot.send_message("The heist was a failure. #Rigged")


def start_heist(bot, user, bet=None, *args):
	global heist

	if bet is None:
		bot.send_message("You need to specify an amount to bet. !heist <amount>")

	else:
		try:
			bet = int(bet)

		except ValueError:
			bot.send_message("That's not a valid bet.")
		
		else:
			if bet < 1:
				bot.send_message("You need to bet at least 1 coin.")

			else:
				if heist is None:
					heist = Heist()

				heist.add_user(bot, user, bet)


def run_heist(bot):
	heist.start(bot)


def end_heist(bot):
	global heist

	heist.end(bot)
	heist = None