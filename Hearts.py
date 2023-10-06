from Deck import Deck, Card, Suits
import random

from Player import Player

class HeartsFunctions():
    def __init__(self):
        pass
        
    def end_trick(self, trick, players):
        lead_suit = trick[0].suit
        suited_trick = self.check_suit(trick, lead_suit)
        highest_card = self.get_highest_card(suited_trick, lead_suit)
        player_who_won_trick = players[trick.index(highest_card)]
        self.count_points_for(player_who_won_trick, trick)
        return f"{player_who_won_trick.name}, {player_who_won_trick.points} points won the trick."

    def check_suit(self, cards, suit):
        list = []
        for card in cards:
            if card.suit == suit:
                list.append(card)
        return list

    def count_points_for(self, player, trick):
        for card in trick:
            if card.suit == Suits.Hearts:
                player.add_points(1)
            if card.suit == Suits.Spades and card.rank == 12:
                player.add_points(13)

    def get_highest_card(self, trick, lead_suit):
        highest_card_value = max(card.rank for card in trick if card.suit == lead_suit)
        for card in trick:
            if card.rank == highest_card_value:
                return card 
            
    def reorder_players(starting_player, players):
        starting_index = players.index(starting_player)
        return players[starting_index:] + players[:starting_index]