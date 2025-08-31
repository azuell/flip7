import random

class player:
    def __init__(self, name):
        self.name = name
        self.cards = deck()

        self.playing = True
        self.bust = False

        self.round_score = 0
        self.game_score = 0

    def is_playing(self):
        return self.playing

    def pickup(self, deck):
        if (self.confirm_valid_action()):
            card = deck.pickup()
            if (card):
                print(self.name + " picked up " + str(card.value))
                self.check_bust(card)
                if not self.bust:
                    self.round_score += card.value
                self.cards.add(card)
            else:
                print("Failed to pick up a card. The deck is empty")

    def stay(self):
        self.playing = False
        self.game_score += self.round_score
        
    def confirm_valid_action(self):
        if self.bust:
            print("You can't pick up. You have busted out of this round")
            return False
        if not self.playing:
            print("You can't pick up. You stopped playing in this round. Your score is " + str(self.round_score))
            return False
        return True

    def check_bust(self, new_card):
        if (self.cards.check_bust(new_card)):
            # Oh no you busted
            print("Oh no you busted")
            self.playing = False
            self.bust = True
            self.round_score = 0
    
    def print_hand(self):
        self.cards.sort()
        print(self.name + "'s cards: ", end = "")
        self.cards.print()

    def print_round_score(self):
        print(self.name + "'s round score is: " + str(self.round_score))

    def print_game_score(self):
        print(self.name + "'s game score is: " + str(self.game_score))

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
                    print(" [G] see your overall score for this game")
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
                case "G":
                    self.print_game_score()
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
        
class card:
    def __init__(self, name):
        self.name = str(name)
        if str(name).isnumeric():
            self.value = name

    def __lt__(self, other):
        return self.value < other.value

# dict to count each cards?
class deck:
    def __init__(self):
        self.cards = []
        
    def build_deck(self):
        # Manually add 0 card
        self.cards.append(card(0))
        # Add increasing numbers of each card 1-12
        for card_val in range(13):
            for card_num in range(card_val):
                    self.cards.append(card(card_val))

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
    
    def check_bust(self, new_card):
        for card in self.cards:
            if card.name == new_card.name:
                return True
        return False


new_deck = deck()
new_deck.build_deck()
new_deck.shuffle()

game_players = players(["Amy", "James"])

# All players alive
while (game_players.is_remaining_players()):
    for game_player in game_players.player_list:
        if game_player.is_playing():
            game_player.turn(new_deck)

for game_player in game_players.player_list:
    game_player.print_hand()
    game_player.print_round_score()