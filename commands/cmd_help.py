import discord
from os import path
from use import use,get

async def ex(args, message, client, invoke, server):
    c_titel = "Commands"
    content = ""
    f = "FILES/" + "help.txt"
    f2 = "FILES/" + "help_for_N.txt"
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
            finally:
                await client.send_message(message.author, embed=discord.Embed(color=discord.Color.green(), title=c_titel, description=content))

    if path.isfile(f2):
        c2_titel = "Extra commands for the Saucy Bot"

        member = get.member_by_id(server, message.author.id)
        role1 = discord.utils.get(server.roles, name="Im A Big Boy")
        role2 = discord.utils.get(server.roles, name="Im A Big Girl")

        if role1 in member.roles or role2 in member.roles:
            with open(f2) as f2:
                content2 = f2.read()
            await client.send_message(message.author,embed=discord.Embed(color=discord.Color.orange(), title=c2_titel, description=content2))
