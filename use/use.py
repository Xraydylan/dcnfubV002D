import discord
from discord import Game, Embed
import os
from os import path

async def error(content, channel, client):
    await client.send_message(channel, embed=Embed(color=discord.Color.red(), description=content))

async def assign_role(rolename, message, client, channel, member, server):
    role = discord.utils.get(server.roles, name=rolename)
    if role == None:
        await error("Something went wrong with the role assignment", message.channel, client)
    else:
        if role in member.roles:
            await error("You already have that role.", message.channel, client)
            return False
        else:
            await client.add_roles(member, role)
            await client.send_message(member, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou are now part of: \n%s!" % role.name))
            return True
    return None

async def dev_authorisation_type1(server, member):
    if path.isfile("SETTINGS/" + server.id + "/permission_type1.txt"):
        with open("SETTINGS/" + server.id + "/permission_type1.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        for x in member.roles:
            if x.name in content:
                return True
    return False

async def dev_authorisation_type2(server, member):
    if path.isfile("SETTINGS/" + server.id + "/permission_type2.txt"):
        with open("SETTINGS/" + server.id + "/permission_type2.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        for x in server.members:
            if (x.id in content) and (member.id in content):
                return True
    return False

