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
        async def card(ctx: commands.Context, rank, of, suit):
            card = Card(suit, rank)
            await ctx.send(card)
            
        @self.command()
        async def hearts(ctx: commands.Context, p1, p2, p3, p4):
            self.game = SimpleGame([p1, p2, p3, p4])
            self.game.start_game()
            await ctx.send("Game started!")
            
        @self.command()
        async def play(ctx: commands.Context, rank, of, suit):
            player = self.game.players[self.count]
            self.count += 1
            await ctx.send(f"{player.name} played: {player.play_card(rank, suit)}, Count = {self.count}")
            self.trick.append(Card(suit, rank))
            if self.count >= 4:
                self.count = 0
                await ctx.send(self.hearts.end_trick(self.trick, self.game.players[self.count]))
                
            
        @self.command()
        async def print_player(ctx: commands.Context):
            await ctx.send(f"{self.game.players[self.count]}")
            
        @self.command()
        async def print_game(ctx: commands.Context):
             print(f"{self.game}")
             await ctx.send(f"{self.game}")

class SimpleGame():
    def __init__(self, player_names):
        self.players = [
            Player(player_names[0]),
            Player(player_names[1]),
            Player(player_names[2]),
            Player(player_names[3]),
        ]
        self.deck = Deck()
        
    def start_game(self):
        # self.deck.shuffle()

        for player in self.players:
            player.receive_cards(self.deck.draw(13))
            player.sort_hand()
    
    def __repr__(self):
        return "Simple Game"

bot = HeartsBot()

bot.run(TOKEN)