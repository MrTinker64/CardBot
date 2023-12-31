from Deck import Deck, Card, Suits

class Player:
    def __init__(self, name, user):
        self.name = name
        self.hand = []  # This will hold the player's cards.
        self.score = 0
        self.user = user
        
    def receive_cards(self, cards):
        self.hand += cards
        
    def play_card(self, rank, suit):
        card = Card(suit, rank)
        for card_in_hand in self.hand:
            if card.__dict__ == card_in_hand.__dict__:
                self.hand.remove(card_in_hand)
                return card
        
        raise ValueError(f"{card} not in player's hand!")
        
    def sort_hand(self):
        self.hand.sort(key=lambda card: (Deck.SUITS.index(card.suit), Deck.RANKS.index(card.rank)), reverse=True)
                
    def add_points(self, points):
        self.score += points
        
    def check_for_suit(self, suit: Suits):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False
        
    def __repr__(self):
        return f"{self.name}, {self.score} points: {self.hand}"
    
if __name__ == "__main__":
    deck = Deck()
    player1 = Player("Avi")
    player1.receive_cards(deck.draw(13))
    player1.sort_hand()
    
    rank, of, suit = input(f"{player1}, play a card: ").split()
    player1.play_card(rank, suit)
    
