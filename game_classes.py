import pygame, sys
from pygame.locals import *
import random
import time


'''Creates buttons that when mouse is over it, it turns color'''

class Button_Hover:
    hovered = False

    def __init__(self, text, pos, screen, placement):
        self.text = text
        self.pos = pos
        self.placement = placement
        self.set_rect()
        self.draw(screen)

    def draw(self, screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        menu_options_font = pygame.font.Font(None, 40)
        self.rend = menu_options_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return pygame.Color("white")
        else:
            return pygame.Color("black")

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        if self.placement == "topleft":
            self.rect.topleft = self.pos
        elif self.placement == "center":
            self.rect.center = self.pos
        elif self.placement == "midtop":
            self.rect.midtop = self.pos

    def check_hover(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            self.draw(screen)
            return True
        else:
            self.hovered = False
            self.draw(screen)
            return False



'''Get a card'''

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.selected = False
        self.ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Joker']
        if self.suit == "Clubs" or self.suit == "Spades" or self.rank == 'Black_Joker':
            self.color = "Black"
        else:
            self.color = "Red"

    def get_name(self):
        if (self.suit == 'None'):
            return self.rank
        else:
            return self.ranks[self.rank - 1] + '_of_' + self.suit

    def __repr__(self):
        return self.get_name()

    def is_selected(self):
        return self.selected

    def toggle_selected(self):
        if (self.selected == False):
            self.selected = True
        else:
            self.selected = False



'''Make a deck'''

class Deck:
    def __init__(self):
        self.remainingCards = []
        self.dealtCards = []
        num_decks = 5  # Adding a specific number of decks
        for i in range(num_decks):
            for suit in ['Hearts', 'Spades', 'Diamonds', 'Clubs']:
                for rank in range(1, 14):
                    self.remainingCards.append(Card(rank, suit))
            self.remainingCards.append(Card('Black_Joker', 'None'))
            self.remainingCards.append(Card('Red_Joker', 'None'))

    def shuffle(self):
        return random.shuffle(self.remainingCards)

    def deal_card(self):
        self.dealtCards.append(self.remainingCards.pop())
        return self.dealtCards[-1].get_name()

    def get_card(self):
        self.dealtCards.append(self.remainingCards.pop())
        return self.dealtCards[-1]

    def get_size(self):
        return len[self.remainingCards]



'''Define Players'''

class Player:
    def __init__(self, deck):
        # Initialise players hand and foot via given deck
        self.on_Hand = True
        self.hand = []
        self.foot = []
        self.canastas = []
        # Deals two sets of 14 cards to the player
        for i in range(13):
            self.hand.append(deck.get_card())
            self.foot.append(deck.get_card())

    # Returns the players hand
    def get_hand(self):
        return self.hand

    # Returns true if the player is on their hand, and false if their on their foot
    def on_hand(self):
        return self.on_Hand

    # When the hands cards run out, this should be toggled to indicate that the player is not on their foot
    def change_to_foot(self):
        self.on_Hand = False

    # Returns 2D array of canastas
    def get_canastas(self):
        return self.canastas

    # Returns a list of selected cards in the hand
    def get_selected_cards(self):
        selected_cards = []
        for item in self.hand:
            if (item.is_selected()):
                selected_cards.append(item)
                item.toggle_selected()
        return selected_cards

    # Call with a single card object and it will remove it from the hand or foot
    # If the hand becomes empty, it switches the bool on_Hand to be False
    # And also transfers the cards from the foot into the hand
    def remove_card(self, card_name):
        self.hand.remove(card_name)
        if (self.on_Hand) and (len(self.hand) == 0):
                self.on_Hand = False
                self.hand = self.foot
        else:
            pass
            #if (len(self.foot) == 0):
            #    END GAME

    # Given a card it will append it to the end of the hand
    def add_card(self, card_name):
        self.hand.append(card_name)

    # Take passed in array of cards and attempts to make a canasta
    # Will return False for invalid canasta's and True for valid canasta's
    def make_canasta(self, cards):
        if len(cards) < 3:
            print("Must have at least 3 elements to create a canasta")
            return False
        temp_cards = []
        numCards = 0
        numWildCards = 0
        for c in cards:
            card = c.get_name()
            if card == "Black_Joker" or card == "Red_Joker" or card == "2_of_Clubs" or card == "2_of_Diamonds" or card == "2_of_Hearts" or card == "2_of_Spades":
                numWildCards = numWildCards + 1
            else:
                temp_cards.append(c)
        if (numWildCards == len(cards)):
            print("Cannot make a canasta of all wildcards")
            return False
        cardType = temp_cards[0].get_name()[0]
        for card in temp_cards:
            if card.get_name()[0] == cardType:
                numCards = numCards + 1
        if numCards != len(temp_cards):
            print("All card that are not wildcards must be of the same type")
            return False
        if numWildCards >= numCards:
            print("Cannot create a canasta with the same or more wildcards then regular cards")
            return False
        self.canastas.append(cards)
        return True

    # Will attempt add selected cards to the index'th canasta, if possible and valid
    def add_to_canasta(self, index):
        # Identify the type of the selected canasta
        card_type = "N"
        for c in self.get_canastas()[index]:
            card = c.get_name()
            if not (card == "Black_Joker" or card == "Red_Joker" or card == "2_of_Clubs" or card == "2_of_Diamonds" or card == "2_of_Hearts" or card == "2_of_Spades"):
                card_type = card[0]
        # Attempt to add selected cards to that canasta
        temp_disc_deck = self.get_selected_cards()
        for c in temp_disc_deck:
            # Deals with adding cards of the index'th canasta's type to the canasta
            if (c.get_name()[0] == card_type):
                self.canastas[index].append(c)
                self.remove_card(c)
            # Deals with adding wildcards to a canasta + Checking there will not be too many
            elif (c.get_name() == "Black_Joker" or c.get_name() == "Red_Joker" or c.get_name() == "2_of_Clubs" or c.get_name() == "2_of_Diamonds" or c.get_name() == "2_of_Hearts" or c.get_name() == "2_of_Spades"):
                numWildCards = 0
                for cards in self.get_canastas()[index]:
                    cards = cards.get_name()
                    if cards == "Black_Joker" or cards == "Red_Joker" or cards == "2_of_Clubs" or cards == "2_of_Diamonds" or cards == "2_of_Hearts" or cards == "2_of_Spades":
                        numWildCards = numWildCards + 1
                if (numWildCards + 1 < len(self.get_canastas()[index]) - numWildCards):
                    print(numWildCards)
                    self.canastas[index].append(c)
                    self.remove_card(c)

    #logic for the computer players to take their turn
    def take_turn(self):
        #keep a count of each type of card
        cardCounter = [0] * 14
        numWildCards = 0
        #loop through cards in hand to see if a cards can be added to a canasta, also take a count of each type of card to see if a new canasta can be made
        for i in self.hand:
            card = i
            cardName = card.get_name()
            cardRank = card.rank
            if not (cardName == "Black_Joker" or cardName == "Red_Joker" or cardName == "2_of_Clubs" or cardName == "2_of_Diamonds" or cardName == "2_of_Hearts" or cardName == "2_of_Spades"):
                for k in self.canastas:
                    if card in self.canastas[k]:
                        #add card to the K'th canasta and remove from that players hand
                        self.i.toggle_selected()
                        self.add_to_canasta(k)
                        self.remove_card(i)
                        #return
                cardCounter[cardRank-1] = cardCounter[cardRank-1] + 1
            else:
                numWildCards = numWildCards + 1 
        print(cardCounter)
        #if no existing canasta exist that cards can be added to, see if you can make new canastas
        iteration = 0
        for numCards in cardCounter:
            if numCards >= 3:
                #loop through hand to select all cards of same type and attempt to make canasta
                for i in self.hand:
                    if i.rank == "Black_Joker" or i.rank == "Red_Joker":
                        continue
                    if i.rank-1 == iteration:
                        i.toggle_selected()
                selectedCards = self.get_selected_cards()
                print(selectedCards[0].get_name())
                if self.make_canasta(selectedCards):
                    for pos in range(len(selectedCards)):
                        self.remove_card(selectedCards[pos])

            iteration = iteration + 1 
            
        
        #discard a red 3 first, then a black 3 then lowest valued card in hand 
            
        




