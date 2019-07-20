from Player import Player
from Hand import Hand
from Deck import Deck
from Pot import Pot
from random import choice, randint

'''
Function used by both classes. Return the object of the next player to bid.
'''
def get_next_player(prev_player, all_players, players_left):
	prev_player_index = player_index(prev_player, all_players)
	next_player_index = prev_player_index + 1 % len(all_players) # get next player index
	while next_player_index < len(all_players):
		if all_players[next_player_index] in players_left:
			return all_players[next_player_index]
		next_player_index += 1
			
	return all_players[0]

'''
Return the index of the given player in the list of players.
'''
def player_index(player, players):
	player_ids = [p.id for p in players]
	if player.id in player_ids:
		return player_ids.index(player.id)
	else:
		raise Exception('Player does not exist with id', id_)

'''
Return the player object with the given id_.
'''
def player_from_id(id_, players):
	objects = [player for player in players if player.id == id_]
	if objects:
		return objects[0]
	else:
		raise Exception('Player does not exist with id', id_)


############################################################################


class Poker:

	def __init__(self, start_money):
		# game objects
		self.players = list()
		self.players_left = list() # players who have not gone bankrupt
		# game information
		self.dealer = None
		self.starting_money = start_money

	'''
	Initialize game by setting up player objects and dealing cards.
	'''
	def initialize(self):
		# generate players
		num_players = input('Welcome to Poker! How many players are playing? ')
		print('\nPlayers start with', self.starting_money, 'dollars')
		for i in range(int(num_players)):
			self.players.append(Player(i+1, self.starting_money)) # players hard-coded to start with $20
		self.players_left = self.players.copy() # important so modifications to one don't affect the other
		self.dealer = choice(self.players)
		print(' - Player', self.dealer.id, 'is chosen as the dealer')

	def remove_bankrupt_players(self):
		# determine bankrupt players
		bankrupt_players = list()
		for player in self.players_left:
			if player.money == 0:
				print('Player', player.id, 'has gone bankrupt')
				bankrupt_players.append(player)

		# remove players
		for bankrupt_player in bankrupt_players:
			self.players_left.remove(bankrupt_player)

	def play(self):
		self.initialize()
		while len(self.players_left) > 1:
			print('Starting a new round!')
			this_round = Round(self, self.players_left)
			this_round.play()
			self.remove_bankrupt_players() # remove any players who have gone bankrupt

			# set next dealer in game
			self.dealer = get_next_player(self.dealer, self.players, self.players_left)

		print('Player', self.players_left[0].id, 'you are the winner!')
			

############################################################################


'''
A round ends when all 5 cards have been dealt and all hands scored.
'''
class Round:

	'''
	Initialize game information. Players assumed to sit by increasing player number clockwise.
	'''
	def __init__(self, game, players):
		# game information
		self.game = game
		self.deck = Deck() # new deck created for each round
		self.minimum_bid = 2 # hard-coded minimum bet
		# round-specific information
		self.pot = Pot() # pot holds community cards and money for the round
		self.player_order = self.set_player_order(players)
		self.folded_players = list()
		# betting order information
		self.small_blind = get_next_player(game.dealer, self.player_order, self.active_players)
		self.big_blind = get_next_player(self.small_blind, self.player_order, self.active_players)
		self.betting_player = None

	'''
	Return list of player objects in the order that they will play.
	'''
	def set_player_order(self, players):
		id_order = [num for num in range(self.game.dealer.id+1, len(players)+1)] + [num for num in range(1, self.game.dealer.id+1)] # include all ids
		player_ids = [player.id for player in players] # include only ids of players in round
		return [player_from_id(id_, players) for id_ in id_order if id_ in player_ids] # filter to get only players in the round

	'''
	Big and little blind are forced to make bids.
	Players are assumed to sit in number order clockwise.
	Play starts to the left of the dealer.
	(i.e., if 5 players are playing and player 2 is the dealer, player 1 = the small blind, player 5 = the big blind)
	'''
	def do_blinds(self):
		made_small_blind = self.small_blind.force_blind('small', self.pot, self.minimum_bid//2)
		if not made_small_blind:
			self.add_folded_player(self.small_blind, True)
		
		made_big_blind = self.big_blind.force_blind('big', self.pot, self.minimum_bid)
		if not made_big_blind:
			self.add_folded_player(self.big_blind, True)

		# set next player
		self.betting_player = get_next_player(self.big_blind, self.player_order, self.active_players)

	'''
	Cards are dealt to each player.
	'''
	def pre_flop(self):
		for player in self.player_order:
			new_hand = Hand(self.deck.deal(2))
			player.deal_hand(new_hand)

	'''
	Conducts 1 round of betting until all players have checked or folded (aka pot is balanced).
	Takes in prev_player, the most recent player to have bid.
	'''
	def betting(self, pot_balanced):
		if self.winner() is not None:
			return

		print('Betting now begins with player', self.betting_player.id)
		# if pot_balanced, give players the chance to bet
		if pot_balanced:
			# get an action from all players still in the round
			for i in range(len(self.active_players)):
				next_up = get_next_player(self.betting_player, self.player_order, self.active_players) # get next_up first, in case self.betting_player folds
				self.betting_player.action(self) # pass in current round as parameter
				self.betting_player = next_up
				if self.winner() is not None:
					return

		# if all players have made an action and the pot is not balanced, continue around
		while not self.pot.balanced():
			next_up = get_next_player(self.betting_player, self.player_order, self.active_players) # get next_up first, in case self.betting_player folds
			self.betting_player.action(self) # pass in current round as parameter
			self.betting_player = next_up
			if self.winner() is not None:
				return

	'''
	Deal 3 cards face-up from the deck and show to players.
	'''
	def flop(self):
		if self.winner() is not None:
			return
		print('3 cards are now dealt face-up')
		flop_cards = self.deck.deal(3)
		self.pot.add_cards(flop_cards)
		print([card.__str__() for card in flop_cards], '\n')

	'''
	Flip over a new card and show it to players.
	'''
	def show_card(self):
		if self.winner() is not None:
			return
		print('Another card is dealt')
		face_up_card = self.deck.deal(1)
		self.pot.add_cards(face_up_card)
		print([card.__str__() for card in self.pot.cards], '\n')
	
	'''
	Returns players who have not folded in the round.
	'''
	@property
	def active_players(self):
		return [player for player in self.player_order if player not in self.folded_players]

	'''
	Remove player object from lists of players still in the round.
	'''
	def add_folded_player(self, player, remove_from_game = False):
		self.folded_players.append(player)
		if remove_from_game:
			self.game.players_left.remove(player)

	'''
	Check if there is a winner (i.e., just one player who has not folded)
	'''
	def winner(self):
		return self.active_players[0] if len(self.active_players) == 1 else None

	'''
	Score players' hands and reward winner.
	'''
	def score_player_hands(self):
		if self.winner() is not None:
			return self.winner()
		else:
			scores = {}
			for player in self.active_players:
				score, best_hand = player.hand.score_hands(self.pot.cards)
				scores[score] = player
				print(' - Player', player.id, 'uses the hand', best_hand)
			max_score = max(scores.keys())
			winner = scores[max_score]
		return winner

	def give_out_winnings(self, winner):
		print('Player', winner.id, 'wins this round! \n')
		self.pot.reward_winner(winner) # add pot money to winner

		# print everyone in the round's balance (including those who have folded)
		for player in self.player_order:
			print('Player', player.id, 'you have', player.money, 'dollars')
		print('\n####################\n')

	'''
	Play poker.
	'''
	def play(self):
		self.do_blinds()
		self.pre_flop() # deal 2 cards to each player
		self.betting(pot_balanced=False)

		self.flop() # deal 3 cards face-up
		self.betting(pot_balanced=True)

		for i in range(2):
			self.show_card() # each iteration, another card is shown
			self.betting(pot_balanced=True)

		# score player's hands, return winner
		winner = self.score_player_hands()
		self.give_out_winnings(winner)

#################################################################

game = Poker(4)
game.play()


