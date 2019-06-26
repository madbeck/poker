from collections import defaultdict

'''
Pot keeps track of each player's bids and community cards
'''
class Pot:

	def __init__(self):
		# pot starts with 
		self.money = defaultdict(lambda: 0)
		self.folded_money = 0 # any money belonging to folded players
		self.cards = list()

	def add_bet(self, player, money):
		self.money[player] += money

	def add_cards(self, cards):
		for card in cards:
			self.cards.append(card)

	'''
	Return true if all the player's money in the pot is the same
	'''
	def balanced(self):
		if not self.money: # pot is empty
			return True
		a_value = list(self.money.values())[0]
		return all(value == a_value for value in self.money.values())

	'''
	Return amount needed to call for a specific player
	'''
	def amount_to_call(self, player):
		highest_bid = max(value for value in self.money.values())
		return highest_bid - self.money[player]

	'''
	Remove folded player, adding their money to self.folded_money
	'''
	def remove_player(self, player):
		player_money = self.money[player] # works??
		self.folded_money += player_money
		del self.money[player]

	def reward_winner(self, player):
		winnings = sum(self.money.values()) + self.folded_money
		player.add_winnings(winnings)

