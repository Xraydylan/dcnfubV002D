import discord
from use import use,get
import os
from os import path
import CONECT
import dropbox

initial = 0

async def ex(args, message, client, invoke, server):
    global initial
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")

        if initial == 0:
            if not path.isfile("SETTINGS/" + server.id + "/permission.txt"):
                out = open("SETTINGS/" + server.id + "/permission.txt", 'w')
                out.write("0\n")
                out.close()
            initial = 1

        if await use.dev_authorisation(client, server, get.member_by_message(server, message)):
            if args_out == "ping":
                await client.send_message(message.channel, "dev Pong!")
            elif args_out == "pull authorisation":
                await pull_authorisation(client, server, message.channel)

        else:
            await use.error("You don´t have the right permission to do this.", message.channel, client)

    else:
        await use.error("The command is not valid.", message.channel, client)

async def pull_authorisation(client,server,channel):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    metadata, f = dbx.files_download("/Gear_Two/permission.txt")
    out = open("SETTINGS/" + server.id + "/permission.txt", 'wb')
    out.write(f.content)
    out.close()
    await client.send_message(channel, "Updating permissions")