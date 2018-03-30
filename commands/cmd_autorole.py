import os
from os import path

import discord


async def error(content, channel, client):
    await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))


def get(server):
    f = "SETTINGS/" + server.id + "/autorole"
    if path.isfile(f):
        with open(f) as f:
            return discord.utils.get(server.roles, id=f.read())
    else:
        return None


def saveFile(id, server):
    if not path.isdir("SETTINGS/" + server.id):
        os.makedirs("SETTINGS/" + server.id)
    with open("SETTINGS/" + server.id + "/autorole", "w") as f:
        f.write(id)
        f.close()


async def ex(args, message, client, invoke):

    rolea = discord.utils.get(message.server.roles, name="The One and Only")
    roleb = discord.utils.get(message.server.roles, name="Bot Master")
    if (rolea in message.author.roles) or (roleb in message.author.roles):
        print("permission")
        if len(args) > 0:
            rolename = args.__str__()[1:-1].replace(",", "").replace("'", "")
            role = discord.utils.get(message.server.roles, name=rolename)
            if role == None:
                await error("Please enter a valid role existing on this server!", message.channel, client)
            else:
                try:
                    saveFile(role.id, message.server)
                    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Successfully set autorole to role `%s`" % role.name)))
                except Exception:
                    await error("Something went wrong while saving autorole!", message.channel, client)
                    raise Exception
    else:
        await error("You don´t have the right permission to do this.\nYou need role %s or %s to do this" % (rolea.mention, roleb.mention), message.channel, client)