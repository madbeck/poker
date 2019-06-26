import itertools
import operator
from collections import Counter
from Deck import Deck
from Card import Card

'''
Player's hand (2 cards)
'''
class Hand(object):

	def __init__(self, cards, game = None):
		self.cards = cards # array of 2 cards
		self.game = game

	def __repr__(self):
		return repr([card for card in self.cards])

	def __str__(self):
		return str([card.__str__() for card in self.cards])

	'''
	Find all possible hands with pot_cards and score them. Return the hand with the best score.
	'''
	def score_hands(self, pot_cards):
		score, best_hand = 0, None
		all_cards = list([i for i in pot_cards] + [j for j in self.cards])
		hands_to_score = [FinalHand(hand) for hand in list(itertools.combinations(all_cards, 5))]
		
		for hand in hands_to_score:
			curr_score = hand.score_hand()
			if curr_score > score:
				score = curr_score
				best_hand = hand

		return score, best_hand


##################################################################

'''
Final hand (5 cards) used to determine winner at the end of each round
'''
class FinalHand(object):

	def __init__(self, cards):
		if (len(cards)) != 5:
			print('Final hands must have 5 cards!')
		self.cards = sorted(cards)
		self.counter = Counter([card.value for card in self.cards]) # dictionary with counts of each card

	def __str__(self):
		return str([card.__str__() for card in self.cards])

	def score_hand(self):
		score = 0

		# pre-calculate all hand possibilities
		royal_flush = self.royal_flush()
		straight_flush = self.straight_flush()
		four_of_a_kind, kind = self.four_of_a_kind()
		full_house, highest_rank = self.four_of_a_kind()
		flush, high_card = self.flush()
		straight, high_card = self.straight()
		three_of_a_kind, kind = self.three_of_a_kind()
		two_pair, high_pair = self.two_pair()
		one_pair, pair = self.one_pair()
		highest_card = self.high_card()

		# calculate hand score
		if royal_flush:
			score += 10		
		elif straight_flush:
			score += 9 + (highest_card / 100)
		elif four_of_a_kind:
			score += 8 + (kind / 100)
		elif full_house:
			score += 7 + (highest_rank / 100)
		elif flush:
			score += 6 + (high_card / 100)
		elif straight:
			score += 5 + (high_card / 100)
		elif three_of_a_kind:
			score += 4 + (kind / 100)
		elif two_pair:
			score += 3 + (high_pair / 100) + (highest_card / 1000) # add highest card in case of a tie
		elif one_pair:
			score += 2 + (pair / 100) + (highest_card / 1000)
		else:
			score += 1 + (self.high_card() / 100)

		return score

	'''
	Returns the nth most repeated card.
	'''
	def get_repeated_card(self, n):
		# most_common(5) returns a list of the 5 most common elements and their counts
		return self.counter.most_common(5)[n-1]

	def royal_flush(self):
		flush, high_card = self.flush()
		return flush and all(card.value in [10, 11, 12, 13, 14] for card in self.cards)

	def straight_flush(self):
		flush, high_card = self.flush()
		straight, high_card = self.straight()
		return straight and flush

	def four_of_a_kind(self):
		return max(self.counter.values()) == 4, max(self.counter.items(), key=operator.itemgetter(1))[0]

	def full_house(self):
		return self.get_repeated_card(1)[1] == 3 and self.get_repeated_card(2)[1] == 2, self.get_repeated_card(2)[0]

	def flush(self):
		a_suit = self.cards[0].suit
		return all(card.suit == a_suit for card in self.cards), self.high_card()

	def straight(self):
		prev = self.cards[0]
		for card in self.cards:
			if card != prev and card.value != prev.value + 1:
				return False, self.high_card()
			prev = card

		return True, self.high_card()

	def three_of_a_kind(self):
		return max(self.counter.values()) == 3, max(self.counter.items(), key=operator.itemgetter(1))[0]

	def two_pair(self):
		return self.get_repeated_card(1)[1] == 2 and self.get_repeated_card(2)[1] == 2, self.get_repeated_card(2)[0]

	def one_pair(self):
		return self.get_repeated_card(1)[1] == 2, self.get_repeated_card(1)[0]

	'''
	Return value of highest card
	'''
	def high_card(self):
		return max([card.value for card in self.cards])

#################################################################

'''
h = Hand([Card(11, 'Clubs'), Card(10, 'Spades')])
score, bh = h.score_hands([Card(3, 'Spades'), Card(9, 'Clubs'), Card(13, 'Hearts'), Card(10, 'Clubs'), Card(14, 'Spades')])

royal_flush = FinalHand([Card(11, 'Hearts'), Card(10, 'Hearts'), Card(12, 'Hearts'), Card(13, 'Hearts'), Card(14, 'Hearts')])
print(royal_flush.royal_flush())

straight_flush = FinalHand([Card(8, 'Hearts'), Card(9, 'Hearts'), Card(10, 'Hearts'), Card(11, 'Hearts'), Card(12, 'Hearts')])
print(straight_flush.straight_flush())

four_of_a_kind = FinalHand([Card(11, 'Hearts'), Card(11, 'Spades'), Card(11, 'Diamonds'), Card(13, 'Hearts'), Card(11, 'Clubs')])
print(four_of_a_kind.four_of_a_kind())

full_house = FinalHand([Card(11, 'Hearts'), Card(11, 'Spades'), Card(11, 'Diamonds'), Card(13, 'Hearts'), Card(13, 'Clubs')])
print(full_house.full_house())

flush = FinalHand([Card(11, 'Hearts'), Card(12, 'Hearts'), Card(10, 'Hearts'), Card(13, 'Hearts'), Card(13, 'Hearts')])
print(flush.flush())

straight = FinalHand([Card(8, 'Hearts'), Card(9, 'Clubs'), Card(10, 'Spades'), Card(11, 'Hearts'), Card(12, 'Hearts')])
print(straight.straight())

three_of_a_kind = FinalHand([Card(11, 'Hearts'), Card(11, 'Spades'), Card(11, 'Diamonds'), Card(13, 'Hearts'), Card(6, 'Clubs')])
print(three_of_a_kind.three_of_a_kind())

two_pair = FinalHand([Card(11, 'Hearts'), Card(11, 'Spades'), Card(13, 'Diamonds'), Card(13, 'Hearts'), Card(6, 'Clubs')])
print(two_pair.two_pair())

one_pair = FinalHand([Card(13, 'Hearts'), Card(11, 'Spades'), Card(11, 'Diamonds'), Card(4, 'Hearts'), Card(6, 'Clubs')])
print(one_pair.one_pair())

hand = Hand([Card(11, 'Hearts'), Card(10, 'Hearts')])
hand.score_hands([Card(9, 'Spades'), Card(3, 'Hearts'), Card(13, 'Hearts'), Card(14, 'Hearts'), Card(6, 'Diamonds')])
'''

