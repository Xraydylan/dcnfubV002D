import discord
from os import path

async def ex(args, message, client, invoke):
    c_titel = "Commands"
    content = ""
    f = "HELP/" + "help.txt"
    if path.isfile(f):
        with open(f) as f:
            content = f.read()
    await client.send_message(message.author, embed=discord.Embed(color=discord.Color.green(), title=c_titel, description=content))