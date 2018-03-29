# Test Bot gear one test

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os


token = str(os.environ.get('TOKEN'))
bot = commands.Bot(command_prefix = '-')

@bot.event
async def on_ready():
    print ("Bot is on.")
    print (bot.user.name)

@bot.command(pass_context=True)
async def hallo(ctx):
    await bot.say("Hallo back.")

bot.run(token)
