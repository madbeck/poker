from Suits import Suits
from FaceValues import FaceValues

class Card(object):

	def __init__(self, value, suit):
		self.value = value
		self.suit = suit
		self.suit_symbol = Suits.SUITS[self.suit]

	# is self equal to other?
	def __eq__(self, other):
		return isinstance(other, Card) and other.value == self.value and other.suit == self.suit

	# is self greater than other?
	def __gt__(self, other):
		return self.value > other.value

	# representation of object for developer (i.e., Card(value=4, suit='Hearts'))
	def __repr__(self):
		return 'Card(value=%r, suit=%r)' % (self.value, self.suit)

	# representation of object for player
	def __str__(self):
		return str(FaceValues.FACEVALUES[self.value]) + str(self.suit_symbol)

	# return color of card
	def color(self):
		return 'red' if self.suit in [Suits.HEARTS, Suits.DIAMONDS] else 'black'

#####################################################################

'''
c = Card(4, 'Hearts')
print(c.color())
print(repr(c))
print(c)
c = Card(12, 'Clubs')
print(c)
'''


