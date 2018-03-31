import discord
from discord import Game, Embed

import CONECT
from commands import cmd_ping, cmd_hello, cmd_autorole, cmd_NSFWauthorise, cmd_to_role, cmd_help
import STATICS

client = discord.Client()
n_server = None

commands = {

    "ping": cmd_ping,
    "hello": cmd_hello,
    "autorole": cmd_autorole,
    "I´m": cmd_NSFWauthorise,
    "Im": cmd_NSFWauthorise,
    "To": cmd_to_role,
    "to": cmd_to_role,
    "help": cmd_help

}

@client.event
async def on_ready():
    global n_server
    print("Bot is logged in successfully. Running on servers:\n")
    for s in client.servers:
        print("  - %s (%s)" % (s.name, s.id))
        if str(s.id) == "405491215870459914":
            n_server = s
            print (n_server.name)
    await client.change_presence(game=Game(name="Ready to help"))


@client.event
async def on_message(message):
    global n_server
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            await commands.get(invoke).ex(args, message, client, invoke, n_server)
        else:
            await client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("The command `%s` is not valid!" % invoke)))

@client.event
async def on_member_join(member):
    custome_welcome = "Hey there!\nThis is Nerfy\nWelcome to my own Server!\nFeel free to check out all the chats and of course share whatever you wanna share <3\nThx so much for your support! As another Member of the #NerfyArmy you basically joined a small Family here :heart: I Hope you enjoy yout Time here !\nFor now\nSee ya and peace OUT! /)"
    await client.send_message(member, embed=Embed(color=discord.Color.orange(), description=custome_welcome))
    role = cmd_autorole.get(member.server)
    if not role == None:
        await client.add_roles(member, role)
        custome_first_promote="Congratulations!! \n\nYou have been promoted!! \n\nYou are now a part of the %s!!" % role.name
        await client.send_message(member,embed=Embed(color=discord.Color.green(), description=custome_first_promote))



client.run(CONECT.TOKEN)