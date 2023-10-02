# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from Deck import Card, Deck, Suits
from Hearts import HeartsGame
from Player import Player
from secretkey import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def card(ctx, rank, of, suit):
    card = Card(suit, rank)
    await ctx.send(card)
    
@bot.command()
async def hearts(ctx, p1, p2, p3, p4):
    game = HeartsGame([p1, p2, p3, p4])
    game.run_game()
    await ctx.send("Game started!")
    
@bot.command()
async def play(ctx, rank, of, suit):
    p1 = Player("alice")
    deck = Deck()
    p1.receive_cards(deck.draw(1))
    await ctx.send(f"{p1.name} played: {p1.play_card(rank, suit)}")
    
# TODO Send point values at end of round

bot.run(TOKEN)