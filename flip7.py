import random
from enum import Enum

class player_state(Enum):
    PLAYING = 1
    FROZEN = 2
    STAYING = 3
    BUSTED = 4

class player:
    def __init__(self, name):
        self.name = name
        self.cards = deck()

        self.state = player_state.PLAYING

    def is_playing(self):
        return self.state == player_state.PLAYING

    def pickup(self, deck):
        if (self.confirm_valid_action()):
            card = deck.pickup()
            if (card):
                print(self.name + " picked up " + card.name)
                # also move check busting??
                self.check_bust(card)
                self.cards.add(card)
                # check win condition
            else:
                print("Failed to pick up a card. The deck is empty")

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
                    self.pickup(deck)
                    return
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
        for player in self.player_list:
            if player.is_playing():
                # At least one player is still playing
                return True
        return False

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

# dict to count each cards?
class deck:
    def __init__(self):
        self.cards = []
        
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
    
    def add(self, new_card):
        self.cards.append(new_card)
    
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
    
    # number of score cards to try get 7
    
    
new_deck = deck()
new_deck.build_deck()
new_deck.shuffle()

new_deck.print()

game_players = players(["Amy", "James"])

# All players alive
while (game_players.is_remaining_players()):
    for game_player in game_players.player_list:
        if game_player.is_playing():
            game_player.turn(new_deck)

for game_player in game_players.player_list:
    game_player.print_hand()
    game_player.print_round_score()