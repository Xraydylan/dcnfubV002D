import discord
from os import path

async def error(content, channel, client):
    await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

async def ex(args, message, client, invoke, server):
    c_titel = "Commands"
    content = ""
    f = "HELP/" + "help.txt"
    if path.isfile(f):
        with open(f) as f:
            contentpre = f.read()
        role_master = discord.utils.get(server.roles, name="RPG-Master")
        if role_master == None:
            await error("Something in the code went wrong!", message.channel, client)
        else:
            master = next((x for x in server.members if role_master in x.roles))
            try:
                content = contentpre % master.mention
            except:
                await error("Something went wrong!", message.channel, client)
    await client.send_message(message.author, embed=discord.Embed(color=discord.Color.green(), title=c_titel, description=content))