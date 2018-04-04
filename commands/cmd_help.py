import discord
from os import path
from use import use,get

async def ex(args, message, client, invoke, server):
    c_titel = "Commands"
    content = ""
    f = "FILES/" + "help.txt"
    if path.isfile(f):
        with open(f) as f:
            contentpre = f.read()
        rmaster = get.member_by_role(server, discord.utils.get(server.roles, name="RPG-Master"))
        bmaster = get.member_by_role(server, discord.utils.get(server.roles, name="Bot Master"))
        if rmaster == None or bmaster == None:
            await use.error("Something in the code went wrong!", message.channel, client)
        else:
            try:
                content = contentpre % (rmaster.mention, bmaster.mention)
            except:
                await use.error("Something went wrong!", message.channel, client)
    await client.send_message(message.author, embed=discord.Embed(color=discord.Color.green(), title=c_titel, description=content))