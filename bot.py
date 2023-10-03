# This example requires the 'members' and 'message_content' privileged intents to function.

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
        self.game = "_"
        self.count = 0
        self.trick = []
        self.hearts = HeartsFunctions()
        
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
        async def hearts(ctx):
            self.game = SimpleGame()
            self.game.start_game()
            await ctx.send("Game started!")
            
        @self.command()
        async def play(ctx, rank, of, suit):
            game = self.game
            player = game.player
            self.count += 1
            await ctx.send(f"{player.name} played: {player.play_card(rank, suit)}, Count = {self.count}")
            self.trick.append(Card(suit, rank))
            if self.count >= 4:
                self.count = 0
                await ctx.send(self.hearts.end_trick(self.trick, game.player))
                
            
        @self.command()
        async def print_player(ctx):
            await ctx.send(f"{self.game.player}")
            
        @self.command()
        async def print_game(ctx):
             print(f"{self.game}")
             await ctx.send(f"{self.game}")

class SimpleGame():
    def __init__(self):
        self.player = Player("Alice")
        self.deck = Deck()
        
    def start_game(self):
        # self.deck.shuffle()

        self.player.receive_cards(self.deck.draw(13))
        self.player.sort_hand()
    
    def __repr__(self):
        return "Simple Game"

# TODO keep working on shifting methods over from HeartsGame to HeartsBot

bot = HeartsBot()

bot.run(TOKEN)