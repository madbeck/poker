from random import shuffle
from Card import Card
from Suits import Suits

class Deck(object):

	card_suits = Suits.SUITS.keys()

	def __init__(self):
		self.cards = []
		self.create_deck()
		self.shuffle()

	# initialize deck
	def create_deck(self):
		self.cards = [Card(j, i) for i in self.card_suits for j in range(2, 15)]

	# return deck in class format
	def __repr__(self):
		return 'Deck()'

	# return deck in value-suit format
	def __str__(self):
		return str([str(card) for card in self.cards])

	def shuffle(self):
		shuffle(self.cards)

	def deal(self, number_of_cards):
		cards_to_deal = []
		for i in range(number_of_cards):
			cards_to_deal.append(self.cards.pop())
		return cards_to_deal

'''
d = Deck()
print(d)
'''


