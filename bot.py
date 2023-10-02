# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from Deck import Card, Deck, Suits
from Hearts import HeartsGame
from Player import Player
from secretkey import TOKEN

class HeartsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

        @self.event
        async def on_ready():
            print(f'Logged in as {bot.user} (ID: {bot.user.id})')
            print('------')


        @self.command()
        async def card(ctx, rank, of, suit):
            card = Card(suit, rank)
            await ctx.send(card)
            
        @self.command()
        async def hearts(ctx, p1, p2, p3, p4):
            game = HeartsGame([p1, p2, p3, p4])
            game.run_game()
            await ctx.send("Game started!")
            
        @self.command()
        async def play(ctx, rank, of, suit):
            p1 = Player("Alice")
            deck = Deck()
            p1.receive_cards(deck.draw(1))
            await ctx.send(f"{p1.name} played: {p1.play_card(rank, suit)}")
            
        @self.command()
        async def hand(ctx):
            p1 = Player("Alice")
            deck = Deck()
            p1.receive_cards(deck.draw(1))
            await ctx.send(f"{p1}")

bot = HeartsBot()

bot.run(TOKEN)

class HeartsGame():
    def __init__(self, playerNames):
        self.players = [
            Player(playerNames[0]),
            Player(playerNames[1]),
            Player(playerNames[2]),
            Player(playerNames[3]),
        ]
        
    def trick(self, starting_index):
        trick = []
        lead_suit = ""
        count = 1
        player_to_win_trick = self.players[0]
        
        reordered_players = self.players[starting_index:] + self.players[:starting_index]

        for player in reordered_players:
            rank, of, suit = input(f"{player}, play a card: ").split()
            # played_card = random.choice(player.hand)
            # rank, suit = played_card.rank, played_card.suit
            player.play_card(rank, suit)
            trick.append(Card(suit, rank))
            if count == 1:
                lead_suit = suit
            count += 1
        
        print(trick)
        print([player.name for player in reordered_players])
        suited_trick = self.check_suit(trick, lead_suit)
        highest_card = self.get_highest_card(suited_trick, lead_suit)
        player_to_win_trick = reordered_players[trick.index(highest_card)]
        print(f"{player_to_win_trick.name} won the trick")
        self.count_points_for(player_to_win_trick, trick)
        trick.clear
        count = 1
        return player_to_win_trick 

    def run_game(self):
        deck = Deck()
        deck.shuffle()

        for player in self.players:
            player.receive_cards(deck.draw(13))
            player.sort_hand()
            
        starting_player = self.players[0]
        
        first_player = self.trick(self.players.index(starting_player))

        for i in range(12):
            first_player = self.trick(self.players.index(first_player))

        for player in self.players:
            print(player.name, player.points)

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