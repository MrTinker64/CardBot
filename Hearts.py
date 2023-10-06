from Deck import Deck, Card, Suits
import random

from Player import Player

class HeartsFunctions():
    def __init__(self):
        pass
        
    def end_trick(self, trick: list, players: list):
        lead_suit = trick[0].suit
        suited_trick = self.check_suit(trick, lead_suit)
        highest_card = self.get_highest_card(suited_trick, lead_suit)
        player_who_won_trick = players[trick.index(highest_card)]
        self.count_points_for(player_who_won_trick, trick)
        return player_who_won_trick

    def check_suit(cards: list, suit: Suits):
        list = []
        for card in cards:
            if card.suit == suit:
                list.append(card)
        return list

    def count_points_for(self, player: Player, trick: list):
        for card in trick:
            if card.suit == Suits.Hearts:
                player.add_points(1)
            if card.suit == Suits.Spades and card.rank == 12:
                player.add_points(13)

    def get_highest_card(self, trick: list, lead_suit: Suits):
        highest_card_value = max(card.rank for card in trick if card.suit == lead_suit)
        for card in trick:
            if card.rank == highest_card_value:
                return card 
            
    def reorder_players(starting_player: Player, players: list):
        starting_index = players.index(starting_player)
        return players[starting_index:] + players[:starting_index]
    
if __name__ == "__main__":
    players = [
        Player("1", ""),
        Player("2", "")
    ]
    reordered_players = HeartsFunctions.reorder_players(players[0], players)
    for player in reordered_players:
        print(player.name)