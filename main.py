import discord
from discord import Game, Embed
from os import path
import CONECT
from commands import cmd_ping, cmd_hello, cmd_autorole, cmd_NSFWauthorise, cmd_to_role, cmd_help, cmd_server
import STATICS
from use import use,get

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
    "help": cmd_help,
    "server": cmd_server

}

@client.event
async def on_ready():
    global n_server
    print("Bot is logged in successfully. Running on servers:\n")
    for s in client.servers:
        print("  - %s (%s)" % (s.name, s.id))
        if str(s.id) == CONECT.SERVER_ID:
            n_server = s
            print(n_server.name)
    if n_server == None:
        print("No matching server found!")
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
            await use.error(("The command `%s` is not valid!" % invoke), message.channel, client)

@client.event
async def on_member_join(member):
    f = "FILES/" + "join_message.txt"
    if path.isfile(f):
        with open(f) as f:
            custome_welcome = f.read()
        await client.send_message(member, embed=Embed(color=discord.Color.orange(), description=custome_welcome))
    f = "FILES/" + "additional_join_info.txt"
    if path.isfile(f):
        with open(f) as f:
            custome_welcome = f.read()
        await client.send_message(member, embed=Embed(color=discord.Color.blue(), description=custome_welcome))

    role = cmd_autorole.get(member.server)
    if not role == None:
        await client.add_roles(member, role)
        custome_first_promote="Congratulations!! \n\nYou have been promoted!! \n\nYou are now a part of the %s!!" % role.name
        await client.send_message(member,embed=Embed(color=discord.Color.green(), description=custome_first_promote))

client.run(CONECT.TOKEN)