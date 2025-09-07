import random
from enum import Enum

WINNING_SCORE = 200

class player_state(Enum):
    PLAYING = 1
    FROZEN = 2
    STAYING = 3
    FLIPPED7 = 4
    BUSTED = 5

class player:
    def __init__(self, name = None):
        self.name = name
        self.cards = deck()

        self.state = player_state.PLAYING

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        if not isinstance(other, player):
            return NotImplemented
        return str(self) == str(other)

    def new_round(self):
        self.cards = deck()
        self.state = player_state.PLAYING

    def is_playing(self):
        return self.state == player_state.PLAYING

    def pickup(self, deck):
        if (self.confirm_valid_action()):
            card = deck.pickup()
            if (card):
                print(self.name + " picked up " + card.name)
                self.check_bust(card)
                self.cards.add_card(card)
                self.check_win()
                return True
            else:
                print("Failed to pick up a card. The deck is empty")
                return False

    def stay(self):
        self.state = player_state.STAYING
        
    def confirm_valid_action(self):
        match self.state:
            case player_state.FROZEN:
                print("You can't pick up. You got frozen in this round. Your score is " + str(self.calculate_round_score()))
                return False
            case player_state.STAYING:
                print("You can't pick up. You stopped playing in this round. Your score is " + str(self.calculate_round_score()))
                return False
            case player_state.BUSTED:
                print("You can't pick up. You have busted out of this round. You scored 0.")
                return False
            case _:
                return True

    def check_bust(self, new_card):
        if (self.cards.check_bust(new_card)):
            # Oh no you busted
            print("Oh no you busted")
            self.state = player_state.BUSTED
            self.round_score = 0

    def check_win(self):
        if self.state is not player_state.BUSTED and self.cards.unique_number_cards() == 7:
            self.state = player_state.FLIPPED7

    def calculate_round_score(self):
        score = 0
        if self.state != player_state.BUSTED:
            score = self.cards.score()
        return score
    
    def print_hand(self):
        self.cards.sort()
        print(self.name + "'s cards: ", end = "")
        self.cards.print()

    def print_round_score(self):
        self.calculate_round_score()
        print(self.name + "'s round score is: " + str(self.calculate_round_score()) + ", they are " + str(self.state.name))

    # def print_game_score(self):
    #     print(self.name + "'s game score is: " + str(self.game_score))

    def turn(self, deck):
        while True:
            choice = input("What would " + self.name + " like to do? [I] for instructions: ")
            choice = choice.upper()
            
            match choice:
                case "I":
                    print(" [H] for hitting (pickup a card)")
                    print(" [S] to stay (stop playing and cash out your points for this round)")
                    print(" [C] see the cards in your hand")
                    print(" [R] see your score for this round")
                    #print(" [G] see your overall score for this game")
                case "H":
                    return self.pickup(deck)
                case "S":
                    self.stay()
                    return
                case "C":
                    self.print_hand()
                case "R":
                    self.print_round_score()
                # case "G":
                #     self.print_game_score()
                case _:
                    print("Not a valid choice. Try again")

class players:
    def __init__(self, player_names):
        self.player_list = []
        for player_name in player_names:
            self.player_list.append(player(player_name))

    def is_remaining_players(self):
        # Check no one has flipped 7 and someone is still playing
        return not any(x for x in self.player_list if x.state == player_state.FLIPPED7) \
            and any(x for x in self.player_list if x.state == player_state.PLAYING)

    
        # #
        # for player in self.player_list:
        #     if player.is_playing():
        #         # At least one player is still playing
        #         return True
        # return False

class card_type(Enum):
    NUMBER = 1
    MULTIPLIER = 2
    BONUS = 3
    ACTION = 4

class action_card_type(Enum):
    FLIP3 = 1
    FREEZE = 2
    SECONDCHANCE = 3

class card:
    def __init__(self, name, type):
        self.type = type
        match(type):
            case card_type.NUMBER:
                self.name = str(name)
                self.value = name
            case card_type.MULTIPLIER:
                self.name = "x" + str(name)
                self.value = name
            case card_type.BONUS:
                self.name = "+" + str(name)
                self.value = name
            case card_type.ACTION:
                print("action")
            case _:
                print("Invalid card")

    def __lt__(self, other):
        if self.type == card_type.NUMBER and other.type == card_type.NUMBER:
            return self.value < other.value
        return self.name < other.name
    
    def print(self):
        print(self.name)

class deck:
    def __init__(self, blank_deck=True):
        self.cards = []
        if not blank_deck:
            self.build_deck()

    def build_deck(self):
        # Manually add 0 card
        self.cards.append(card(0, card_type.NUMBER))
        
        # Add increasing numbers of each card 1-12
        for card_val in range(13):
            for card_num in range(card_val):
                    self.cards.append(card(card_val, card_type.NUMBER))
        
        # Add bonus point cards
        for bonus_val in range(2, 12, 2):
            self.cards.append(card(bonus_val, card_type.BONUS))
        
        # Add mulitplier card
        self.cards.append(card(2, card_type.MULTIPLIER))
        
        # Finish it all off with a good shuffle
        self.shuffle()

    def print(self):
        for card in self.cards:
            print(card.name, end = "")
            print(", ", end = "")
        print()

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def pickup(self):
        if self.has_cards():
            return self.cards.pop(0)
        # No cards in deck, pickup failed
        return False
    
    def add_card(self, new_card):
        self.cards.append(new_card)

    def add_deck(self, new_deck):
        for new_card in new_deck.cards:
            self.add_card(new_card)
    
    def has_cards(self):
        return (len(self.cards) > 0)
    
    def unique_number_cards(self):
        count = 0
        for card in self.cards:
            if card.type == card_type.NUMBER:
                count += 1
        return count
    
    def score(self):        
        score = 0

        # 1. Add value of number cards
        for number_card in self.cards:
            if number_card.type == card_type.NUMBER:
                score += number_card.value

        # 2. x2 Mulitplier
        if any(x for x in self.cards if x.type == card_type.MULTIPLIER):
            score *= 2

        # 3. Bonus points
        for bonus_card in [x for x in self.cards if x.type == card_type.BONUS]:
            score += bonus_card.value
            
        # 4. Add 15 if flipped 7 number cards
        if self.unique_number_cards() == 7:
            score += 15

        return score
            
    def check_bust(self, new_card):
        for card in self.cards:
            if card.name == new_card.name:
                return True
        return False
    
    def clear_deck(self):
        self.cards = []
    
    # number of score cards to try get 7

class round:
    def __init__(self, players, deck, discard):
        self.players = players
        self.deck = deck
        self.discard = discard

        self.scores = dict()
    
    def round(self):
        print("New round")
        self.deck.print()

        # Reset player hands and states
        for player in self.players.player_list:
            player.new_round()

        # All players alive
        while (self.players.is_remaining_players()):
            for player in self.players.player_list:
                if player.is_playing():
                    self.deck.print()
                    if not self.deck.has_cards():
                        self.deck = self.discard.shuffle()
                        self.discard.clear_deck()
                    player.turn(self.deck)

        # All players dead
        print("The round is over")
        self.deck.print()
        for player in self.players.player_list:
            self.scores[player] = player.calculate_round_score()
            player.print_hand()
            player.print_round_score()
            self.discard.add_deck(player.cards)
            
            
            

        return self.scores
    
    def reset_deck(self):
        used_cards = []


class game:
    def __init__(self, players):
        self.players = players
        
        self.rounds = []
        self.deck = deck(blank_deck = False)

        self.discard = deck(blank_deck = True)

        self.scores = dict()

        self.winning_player = None

    def play(self):
        game_go = True
        while game_go:
            game_round = round(self.players, self.deck, self.discard).round()
            self.rounds.append(game_round)
            for key_player in self.rounds[-1]:
                print(key_player)
                if key_player not in self.scores:
                    self.scores[key_player] = self.rounds[-1][key_player]
                else:
                    self.scores[key_player] += self.rounds[-1][key_player]
                    if not self.winning_player:
                        self.winning_player = key_player
                    
                    if self.scores[key_player] >= self.scores[self.winning_player]:
                        self.winning_player = key_player
                        if self.scores[self.winning_player] > WINNING_SCORE:
                            print(self.winning_player.name + " is the winner with a score of " + str(self.scores[self.winning_player]))
                            game_go = False

players_6 = players(["A", "BB", "CCC", "DDDD", "EEEEE", "FFFFFF"])
players_12 = players(["A", "BB", "CCC", "DDDD", "EEEEE", "FFFFFF", "GGGGGGG", "HHHHHHHH", "IIIIIIIII", "JJJJJJJJJJ", "KKKKKKKKKKK", "LLLLLLLLLLLLL"])
game_players = players(["Amy", "James"])

game(players_6).play()



# there is only ever one of each card!!!
# --> need to update discard alongside busts as they occur
# --> pop all cards over
# need to pass discard alongside decks
# --> mega deck??? - "board" containing deck and discard (and everyone elses hands/states? - will be needed for bot info later on too)
# --> this will also come in handy later on with the second chance cards that need to be discarded upon use
