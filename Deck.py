from enum import Enum
import random


class Suits(Enum):
    Spades = 1
    Hearts = 2
    Diamonds = 3
    Clubs = 4
  
class Card:
    def __init__(self, suit, rank):
        if type(rank) == str:
            rank.lower
            if rank == "jack":
                rank = 11
            elif rank == "queen":
                rank = 12
            elif rank == "king":
                rank = 13
            elif rank == "ace":
                rank = 14
            else:
                rank = int(rank)
        
        if type(suit) == str:
            for suit_enum in Suits:
                if suit_enum.name == suit.lower:
                    suit = suit_enum
                
        self.suit = suit
        self.rank = rank
        
        if rank == 11:
            self.strrank = "Jack"
        elif rank == 12:
            self.strrank = "Queen"
        elif rank == 13:
            self.strrank = "King"
        elif rank == 14:
            self.strrank = "Ace"
        else:
            self.strrank = f"{rank}"

    def __repr__(self):
        return f"{self.strrank} of {self.suit.name}"

class Deck:
    SUITS = [Suits.Clubs, Suits.Diamonds, Suits.Hearts, Suits.Spades]
    RANKS = [2, 3, 4 ,5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]

    def resetDeck(self):
        self.cards.clear
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, numberOfCards):
        drawnCards = []
        for i in range(numberOfCards):
            if self.cards:
                drawnCards.append(self.cards.pop())
            else:
                raise ValueError("Deck is empty!")
        return drawnCards

    def __repr__(self):
        return f"Deck: {self.cards}"

if __name__ == "__main__":
    # Example usage:
    deck = Deck()
    card = deck.draw(13)
    print(card)