# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from Deck import Card
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
    
# TODO Send point values at end of round

bot.run(TOKEN)