'''The code presents a blackjack game between 2 players(Player and Dealer).The aim of the game is to 
get as close to 21points or 21 points without exceeding it. The Player has choices to ask for another card(hit) 
or stand depending on his cards. The dealer has an automated play of hitting till he/she reaches 17 points and stops once he crosses 17 points.
The winner is one who has more number of points(if both have under 21 points).The match is considered draw if both players go over 21 points.'''

#!/usr/bin/env python
# coding: utf-8

# In[2]:


from ast import Is
import random
import os
from IPython.display import clear_output

points = {
    "Ace": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
}
player_choices = {
    1: "Hit",
    2: "Stand",
    3: "Surrender"
}
game_choices = {
    1: "Play again?",
    2: "Reset",
    3: "End Play",
}


class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = [ "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    
    def __init__(self, suit_idx = 0, rank_idx = 2):

        suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
        rank_list = [ "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.suit = suit_list[suit_idx]
        self.rank = rank_list[rank_idx]
        
    def __str__(self):
        return (self.rank + " of " + self.suit)


class Deck:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s += str(self.cards[i]) + "\n"
        return s
    
    def add_deck(self, number_of_decks=1):
        for i in range(number_of_decks):
            for suit in range(4):
                for rank in range(13):
                    self.cards.append(Card(suit, rank))

        print(f"{number_of_decks} decks have been added.")
    
    def shuffle(self):
        n_cards = len(self.cards)
        for i in range(n_cards):

            j = random.randrange(0, n_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        print("Cards have been shuffled.")
            
    def pop_card(self) -> str:
        return self.cards.pop()
    
    def is_empty(self) -> bool:
        return len(self.cards) == 0
    
    def deal(self, player_list, cards_per_player):
        """Add cards to players."""
        if type(player_list) != list:
            player_list = [player_list]
        # Rotating deal for all players. 
        for i in range(cards_per_player):
            if self.is_empty():
                raise ValueError("The deck has run out of cards!")
            for current_player in player_list:
                card = self.pop_card()
                current_player.add_card(card)
                

class Player:
    def __init__(self, name = "", is_dealer = False, is_dealer_revealed = False):
        self.cards = []  # list of cards
        self.name = name
        self.is_dealer = is_dealer
        self.is_dealer_revealed = is_dealer_revealed
        self.points = 0
        
    def add_card(self, card):
        self.cards.append(card)

    def resetplayer(self):
        self.cards = []
        self.points=0
        
    def is_empty(self) -> bool:
        return len(self.cards) == 0
        
    def __str__(self):
        s = "Hand " + self.name
        
        if self.is_empty():
            return s + " is empty"
        s += " contains \n"
        
        if ((self.is_dealer==False) | (self.is_dealer_revealed & self.is_dealer)):
            for i in range(len(self.cards)):
                s += str(self.cards[i].__str__()) + "\n"
        else:
            s += self.cards[0].__str__() + "\n"
            s += "******\n"
        return s

    def calculate_points(self, print_output=True):
        """Calculate the player points"""
        self.points = 0
        ace_count = 0
        for card in self.cards:
            card_number = card.rank
            if card_number == "Ace":
                ace_count += 1
            else:
                self.points += points[card_number]

        for i in range(ace_count):
            if self.points <=10:
                self.points += 11
            else:
                self.points += 1

        if print_output:
            print(f"Points so far: {self.points}\n\n")

        
class Game:

    def __init__(self, player_list):
        self.deck = Deck()
        try:
            self.num_decks = int(input("How many decks do you want to play blackack with?: "))
        except ValueError:
            print("Please enter an integer")
            self.num_decks = int(input("How many decks do you want to play blackack with?: "))
        os.system('cls' if os.name == 'nt' else 'clear')
        self.dealer = Player("Dealer", is_dealer = True)
        self.users = []
        for player in player_list:
            self.users.append(Player(player, False))
        self.create_deck()

    def create_deck(self):
        self.deck.add_deck(self.num_decks)
        self.deck.shuffle()

    def hit_player(self, player):
        """Deal one card to the player."""
        self.deck.deal(player, 1)

    def print_game_state(self):
        """Print the state of the game for the player to understand."""
        print(self.users)
        print(self.dealer)

    def play_for_player(self, player: Player):
        """Allow player to play the game."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(player)
        player.calculate_points()
        print(self.dealer)

        if player.points == 21:
            print("BlackJack!")
        elif player.points>21:
            print("Player Bust!")
        elif player.points<21:
            if player.points < 16:
                print("Suggestion: Please Hit")
            elif player.points >= 19 and player.points <21:
                print("Suggestion: Please Stand")
            elif player.points >=16 and player.points<19:
                print("Suggestion: Hit, But the chances are bleak!")
            choice = 0
            while choice not in [1, 2, 3]:
                try:
                    choice = int(input(f"{player_choices}\nEnter your choice: "))
                except ValueError:
                    print("Please enter a valid choice")
                    choice = int(input(f"{player_choices}\nEnter your choice: "))    
            if choice == 1:
                self.hit_player(player)
                self.play_for_player(player)
            elif choice == 2:
                print("\nDealer will play now")
            elif choice == 3:
                quit_choice = input("Are you sure? (y/n): ")
                if quit_choice == "y":
                    print("Thank you for playing, Unfortunately, you lost your money")
                else:
                    choice = int(input(f"{player_choices}\nEnter your choice: "))    
                    if choice == 1:
                        self.hit_player(player)
                        self.play_for_player(player)
                    elif choice == 2:
                        print("\nDealer will play now")
                    elif choice == 3:
                        quit_choice = input("Are you sure? (y/n): ")
                        if quit_choice == "y":
                            print("Thank you for playing, Unfortunately, you lost your money")
        input("\n\nPress Return to continue to dealer play...")
        os.system('cls' if os.name == 'nt' else 'clear')

        
    def play_for_dealer(self, users):
        """Dealer's Play"""
        self.dealer.calculate_points(print_output=False)
        if self.dealer.points < 17:
            self.hit_player(self.dealer)
            self.play_for_dealer(self.users)
        elif self.dealer.points >= 17 and self.dealer.points <= 20:
            pass
        elif self.dealer.points == 21:
            print("Dealer BlackJack!")
        else:
            print("Dealer Bust")
            
    def decide_winners(self):
        for player in self.users: 
            self.decide_winner(player)

    def decide_winner(self, player):
        """Code to decide the game winner"""
        if player.points  == 21 and self.dealer.points == 21:
            print("match draw")
            print(f"You have got back {bet_amount}!")
        elif player.points == 21 and self.dealer.points != 21:
            print("User Wins")
            print(f"Congratulations you won {bet_amount * 2}!")
        elif player.points != 21 and self.dealer.points == 21:
            print("Dealer Wins")
            print("Sorry you lost your money!")
        elif player.points >21 and self.dealer.points <=21:
            print("Dealer Wins")
            print("Sorry you lost your money!")
        elif player.points <= 21 and self.dealer.points >21:
            print("User Wins")
            print(f"Congratulations you won {bet_amount * 2}!")
        elif player.points >=21 and self.dealer.points >= 21:
            print("match draw")
            print(f"You have got back {bet_amount}!")
        elif player.points < 21 and self.dealer.points < 21:
            if player.points > self.dealer.points:
                print("User wins")
                print(f"Congratulations you won {bet_amount * 2}!")
            elif player.points < self.dealer.points:
                print("Dealer wins")
                print("Sorry you lost your money!")
            elif player.points == self.dealer.points:
                print("Match draw")
                print(f"You have got back {bet_amount}!")

    def play_blackjack(self):
        """Play 1 game of blackjack. """
    
        # Clear hands of players
        for user in (self.users + [self.dealer]):
            user.resetplayer()
            user.is_dealer_revealed = False
        
        # First deal 2 cards to players.
        self.deck.deal(self.users + [self.dealer], cards_per_player=2)
#         self.deck.deal(self.dealer, cards_per_player=2)

        # Game of the all the non-dealer players

        for player in self.users:
            print ("\nPlaying for " + player.name + "\n")
            self.play_for_player(player)

        # Game of the dealer

        print("\nDealer play\n")

        self.play_for_dealer(self.users)
        for player in self.users:
            player: Player
            print(player)
            player.calculate_points()
        self.dealer.is_dealer_revealed = True
        print(self.dealer)
        self.dealer.calculate_points()
        

        # Game Winner is decided
        self.decide_winners()
    
    
    def reset(self):
        """Reset Deck."""
        global bet_amount
        try:
            bet_amount = int(input("How much amount do you want to play blackack with?: "))
        except ValueError: # User enters an integer the second time.
            print("Please enter an integer")
            bet_amount = int(input("How much amount do you want to play blackack with?: "))
        
        self.deck = Deck()
        self.create_deck()
            
        # Reset all players
        for player in self.users:
            player.resetplayer()
        
        # Reset Dealer
        self.dealer.resetplayer()
        self.dealer.is_dealer_revealed = False
        
        # Clear screen & play
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Play again
        self.play_blackjack()
        

if __name__ == '__main__':
    
    # Create players for blackjack
    print("Welcome to Blackjack!")
    player1_name = input("Enter player name: ")
    
    bet_amount = None # Creating variable.
    
    player_name_list = [player1_name]
    
    # Create game object.
    game = Game(player_name_list)
    
    # Resets deck and calls first game.
    game.reset()

    """End game Scenarios"""
    user_choice = 1
    while user_choice != 3:
        try:
            user_choice = int(input(f"\n\n{game_choices}\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid choice")
            user_choice = int(input(f"\n\n{game_choices}\nEnter your choice: "))
            
        if user_choice == 1:
            try:
                bet_amount = int(input("How much amount do you want to play blackack with?: "))
            except ValueError: # User enters an integer the second time.
                print("Please enter an integer")
                bet_amount = int(input("How much amount do you want to play blackack with?: "))
            game.play_blackjack()
        elif user_choice == 2:
            game.reset()
    print("Thank you for playing!")


# In[ ]:





