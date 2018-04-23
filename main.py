import discord
from discord import Game, Embed
from os import path
import CONECT
from commands import cmd_ping, cmd_hello, cmd_autorole, cmd_NSFWauthorise, cmd_to_role, cmd_help, cmd_server, cmd_dev, anti_spam, special_member_count, cmd_com_own, cmd_get_com_own
from commands_2 import uploader,give
import STATICS
from use import use,get
import asyncio
import threading


def Gear_Two():

    n_server = None
    loop_1 = asyncio.new_event_loop()
    client = discord.Client(loop=loop_1)
    commands = {

        "ping": cmd_ping,
        "hello": cmd_hello,
        "autorole": cmd_autorole,
        "I´m": cmd_NSFWauthorise,
        "Im": cmd_NSFWauthorise,
        "To": cmd_to_role,
        "to": cmd_to_role,
        "help": cmd_help,
        "server": cmd_server,
        "dev": cmd_dev,
        #"own":cmd_com_own,
        #"_-":cmd_get_com_own

    }

    uploader_commands = ["uploader", "give"]

    @client.event
    async def on_ready():
        global n_server
        print("Gear_Two is logged in successfully. Running on servers:\n")
        for s in client.servers:
            print("  - %s (%s)" % (s.name, s.id))
            if str(s.id) == CONECT.SERVER_ID:
                n_server = s
                print(n_server.name)
        if n_server == None:
            print("No matching server found!")

        await anti_spam.init_antispam_status(n_server)

        cmd_com_own.download_custom()

        await client.change_presence(game=Game(name="Ready to help"))


    @client.event
    async def on_message(message):
        global n_server
        if anti_spam.status == 1:
            if message.server != None:
                await anti_spam.new_message(client, message, n_server)

        if message.content.startswith(STATICS.PREFIX):
            invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
            args = message.content.split(" ")[1:]
            if invoke == "im":
                invoke = "Im"
            if commands.__contains__(invoke):
                await commands.get(invoke).ex(args, message, client, invoke, n_server)

            elif invoke != "new" and not invoke in uploader_commands:
                await use.error(("The command `%s` is not valid!" % invoke), message.channel, client)

    @client.event
    async def on_member_join(member):
        global n_server
        f = "FILES/" + "join_message.txt"
        if path.isfile(f):
            with open(f) as f:
                custome_welcome = f.read()
            await client.send_message(member, embed=Embed(color=discord.Color.orange(), description=custome_welcome))

        f = "FILES/" + "additional_join_info.txt"
        if path.isfile(f):
            with open(f) as f:
                custome_welcome_pre = f.read()
                custome_welcome = custome_welcome_pre % n_server.member_count
            await client.send_message(member, embed=Embed(color=discord.Color.blue(), description=custome_welcome))

        role = cmd_autorole.get(member.server)
        if not role == None:
            await client.add_roles(member, role)
            custome_first_promote="Congratulations!! \n\nYou have been promoted!! \n\nYou are now a part of the %s!!" % role.name
            await client.send_message(member,embed=Embed(color=discord.Color.green(), description=custome_first_promote))

        await special_member_count.check_count(client, n_server, member)

    client.run(CONECT.TOKEN)

def Picture_Bot():
    n_server = None
    loop_2 = asyncio.new_event_loop()
    client_2 = discord.Client(loop=loop_2)

    commands_2 = {

        "uploader": uploader,
        "give": give,
    }

    @client_2.event
    async def on_ready():
        global n_server
        print("Picture_Bot is logged in successfully. Running on servers:\n")
        for s in client_2.servers:
            print("  - %s (%s)" % (s.name, s.id))
            if str(s.id) == CONECT.SERVER_ID:
                n_server = s
                print(n_server.name)
        if n_server == None:
            print("No matching server found!")
        await uploader.re_status(client_2, asyncio.get_event_loop(), n_server)

    @client_2.event
    async def on_message(message):
        global n_server
        if message.content.startswith(STATICS.PREFIX):
            invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
            args = message.content.split(" ")[1:]
            if commands_2.__contains__(invoke):
                await commands_2.get(invoke).ex(args, message, client_2, invoke, n_server)

    client_2.run(CONECT.TOKEN2)


if __name__ == "__main__":
    thread_gear_two = threading.Thread(name='Gear_Two', target=Gear_Two)
    thread_picture_bot = threading.Thread(name='Picture_Bot', target=Picture_Bot)

    thread_gear_two.start()
    thread_picture_bot.start()
