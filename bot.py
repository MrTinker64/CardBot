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
        self.starting_player = Player("", "")
        self.first_move = True
        self.players = []
        self.lead_suit = Suits.Clubs
        self.end_score = 100
        
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

        @self.event
        async def on_ready():
            print(f'Logged in as {bot.user} (ID: {bot.user.id})')
            print('------')


        @self.command()
        async def test(ctx: commands.Context):
            await ctx.send("Yay!")
            
        @self.command()
        async def hearts(ctx: commands.Context, p2: discord.User, p3: discord.User, p4: discord.User, end_score=100):
            p1 = ctx.author
            self.game = HeartsGame(p1, p2, p3, p4)
            self.end_score = int(end_score)
            await start_game(ctx)
            for player in self.players:
                if player.name == ctx.author.display_name:
                    await ctx.send(f"{player}")
            
        async def start_game(ctx):
            self.starting_player = self.game.start_game()
            self.players = HeartsFunctions.reorder_players(self.starting_player, self.game.players)
            self.first_move = True
            await ctx.send("New round started!")
            
        @self.command()
        async def play(ctx: commands.Context, rank: str, of, suit: str):
            player = self.players[self.count]
            if ctx.author != player.user:
                await ctx.send("It's not your turn!")
                return
            cap_suit = suit.capitalize()
            if self.first_move == True:
                if rank != "2" or cap_suit != "Clubs":
                    await ctx.send("Must play 2 of Clubs!")
                    return
                self.first_move = False
            if self.count != 0:
                if cap_suit != self.lead_suit.name:
                    if player.check_for_suit(self.lead_suit) == True:
                        await ctx.send("You must play on suit!")
                        return
            try:
                await ctx.send(f"{player.name} played: {player.play_card(rank, suit)}")
            except ValueError:
                await ctx.send(f"You don't have that card :|")
                return
            self.count += 1
            self.trick.append(Card(suit, rank))
            if self.count >= 4:
                self.count = 0
                player_who_won_trick = self.hearts.end_trick(self.trick, self.players)
                await ctx.send(f"{player_who_won_trick.name}, {player_who_won_trick.score} points won the trick.")
                self.trick.clear()
                self.players = HeartsFunctions.reorder_players(player_who_won_trick, self.players)
                if len(self.players[0].hand) == 0:
                    for player in self.players:
                        if player.score >= self.end_score:
                            await ctx.send(f"""Game over! Here are the scores:\n
                                                    {self.players[0].name}: {self.players[0].score}\n
                                                    {self.players[1].name}: {self.players[1].score}\n""")
                            return
                    await start_game(ctx)
                
            
        @self.command()
        async def hand(ctx: commands.Context):
            for player in self.players:
                if player.name == ctx.author.display_name:
                    await ctx.send(f"{player}")
            # dm = await bot.create_dm(ctx.author)
            
        @self.command()
        async def print_game(ctx: commands.Context):
             print(f"{self.game}")
             await ctx.send(f"{self.game}")

class HeartsGame():
    def __init__(self, p1: discord.User, p2: discord.User, p3: discord.User, p4: discord.User):
        self.players = [
            Player(p1.display_name, p1),
            Player(p2.display_name, p2),
            Player(p3.display_name, p3),
            Player(p4.display_name, p4)
        ]
        self.deck = Deck()
        
    def start_game(self):
        print("-" * 20, "New game", "-" * 20)
        starting_player = self.players[0]
        self.deck = Deck()
        self.deck.shuffle()

        for player in self.players:
            player.receive_cards(self.deck.draw(13))
            player.sort_hand()
            hf = HeartsFunctions()
            list_of_clubs = hf.check_suit(player.hand, Suits.Clubs)
            for card in list_of_clubs:
                if card.rank == 2:
                    starting_player = player
       
        return starting_player
    
    def __repr__(self):
        return "Simple Game"

bot = HeartsBot()

bot.run(TOKEN)