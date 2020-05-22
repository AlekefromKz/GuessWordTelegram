import telebot
import random
from time import time

CITIES = ['brussels', 'sofia', 'zagreb', 'prague', 'copenghagen', 'tallinn', 'helsinki', 'paris', 'berlin', 'athens', 'budapest', 'dublin', 'rome', 'riga', 'vilnius', 'luxembourg', 'monaco']
# Game states
START = 0
IN_GAME = 1
END = 2

# Responses messages
CORRECT = 0
ALREADY_GUESSED = 1
INCORRECT = 2
NO_GUESSES_LEFT = 3
WON = 4

bot = telebot.TeleBot("TOKEN")

class Game:
	def __init__(self):
		self.secret_word = list(random.choice(CITIES))
		print(self.secret_word)
		self.state = START
		self.guesses_left = 10
		self.dashes = list('-' * len(self.secret_word))
		self.guessed_letters = []

	def check_guess(self, guess):
		if self.guesses_left <= 0:
			return NO_GUESSES_LEFT
		if guess in self.guessed_letters:
			return ALREADY_GUESSED
		if guess in self.secret_word:
			self.update_dashes(guess)
			self.guessed_letters.append(guess)
			if '-' not in self.dashes:
				return WON
			return CORRECT
		else:
			self.guesses_left -= 1
			self.guessed_letters.append(guess)
			if self.guesses_left <= 0:
				return NO_GUESSES_LEFT
			return INCORRECT

	def update_dashes(self, guess):
		for i in range (len(self.dashes)):
			if self.secret_word[i] == guess:
				self.dashes[i] = guess

game_object = None
@bot.message_handler(content_types=['text'])
def send_echo(message):
	global game_object

	if message.text == "start":
		game_object = Game()
		bot.send_message(message.chat.id, "We are in a game. Guesses left: {}. Word: {}".format(game_object.guesses_left, ' '.join(game_object.dashes)))
		game_object.state = IN_GAME
		return

	if not game_object:
		bot.send_message(message.chat.id, "Start a new game by typing 'start'")
		return


	if game_object.state == START:
		bot.send_message(message.chat.id, game_object.secret_word)
		return

	if game_object.state == IN_GAME:
		if len(message.text) > 1:
			bot.send_message(message.chat.id, "Only 1 letter")
			return

		letter = str(message.text).lower()
		result = game_object.check_guess(letter)

		if result == CORRECT:
			bot.send_message(message.chat.id, "Correct: {}. Word: {}".format(letter, ' '.join(game_object.dashes)))
			return
		if result == ALREADY_GUESSED:
			bot.send_message(message.chat.id, "Already guessed letter {}. Word: {}".format(letter, ' '.join(game_object.dashes)))
			return
		if result == INCORRECT:
			bot.send_message(message.chat.id, "Wrong: {}. Guesses left: {}. Word: {}".format(letter, game_object.guesses_left, ' '.join(game_object.dashes)))
			return
		if result == NO_GUESSES_LEFT:
			bot.send_message(message.chat.id, "Wrong: {}. And looks like you lost. The correct answer was: {}".format(letter, ''.join(game_object.secret_word).upper()))
			game_object.state = END
			bot.send_message(message.chat.id, "Do you want to strat a new game?")
			return
		if result == WON:
			bot.send_message(message.chat.id, "Congratulations!!! You won. Word: {}. Guesses left {}".format(''.join(game_object.secret_word).upper(), game_object.guesses_left))
			game_object.state = END
			bot.send_message(message.chat.id, "Do you want to strat a new game?")
			return

	if game_object.state == END:
		letter = message.text
		if letter == 'y' or letter == 'ye' or letter == 'yes':
			game_object = Game()
			bot.send_message(message.chat.id, "Started new game")
			bot.send_message(message.chat.id, "We are in a game. Guesses left: {}. Word: {}".format(game_object.guesses_left, ' '.join(game_object.dashes)))
			game_object.state = IN_GAME
		else:
			bot.send_message(message.chat.id, "Do you want to start a new game?")
		return

print('Started')
bot.polling()