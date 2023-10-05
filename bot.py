# This example requires the 'members' and 'message_content' privileged intents to function.

from typing import List
import discord
from discord.ext import commands
from Deck import Card, Deck, Suits
from Hearts import HeartsFunctions
from Player import Player
from secretkey import TOKEN

class HeartsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.game = HeartsGame(["", "", "", ""])
        self.count = 0
        self.trick = []
        self.hearts = HeartsFunctions()
        self.starting_player = Player("")
        
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

        @self.event
        async def on_ready():
            print(f'Logged in as {bot.user} (ID: {bot.user.id})')
            print('------')


        @self.command()
        async def card(ctx: commands.Context, rank, of, suit):
            card = Card(suit, rank)
            await ctx.send(card)
            
        @self.command()
        async def hearts(ctx: commands.Context, p2: discord.User, p3: discord.User, p4: discord.User):
            p1 = ctx.author
            self.game = HeartsGame(p1, p2, p3, p4)
            self.starting_player = self.game.start_game()
            await ctx.send("Game started!")
            
            # TODO Implement specific rules (ie 2 of Clubs starts)
            
        @self.command()
        async def play(ctx: commands.Context, rank, of, suit):
            player = self.game.players[self.count]
            await ctx.send(f"{player.name} played: {player.play_card(rank, suit)}")
            self.count += 1
            self.trick.append(Card(suit, rank))
            if self.count >= 4:
                self.count = 0
                await ctx.send(self.hearts.end_trick(self.trick, self.game.players[self.count]))
                
            
        @self.command()
        async def hand(ctx: commands.Context):
            for player in self.game.players:
                if player.name == ctx.author.display_name:
                    user = player
            dm = await bot.create_dm(ctx.author)
            await dm.send(f"{user}")
            
        @self.command()
        async def print_game(ctx: commands.Context):
             print(f"{self.game}")
             await ctx.send(f"{self.game}")

class HeartsGame():
    def __init__(self, p1: discord.User, p2: discord.User, p3: discord.User, p4: discord.User):
        self.players = [
            Player(p1.display_name),
            Player(p2.display_name),
            Player(p3.display_name),
            Player(p4.display_name)
        ]
        self.deck = Deck()
        
    def start_game(self):
        starting_player = self.players[0]
        # self.deck.shuffle()

        for player in self.players:
            player.receive_cards(self.deck.draw(13))
            player.sort_hand()
            for card in player.hand:
                if card.suit == Suits.Clubs and card.rank == 2:
                    starting_player == player
       
        return starting_player
    
    def __repr__(self):
        return "Simple Game"

bot = HeartsBot()

bot.run(TOKEN)