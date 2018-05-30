import discord
from discord import Game, Embed
import os
from os import path
import CONECT
import dropbox
from dropbox.files import WriteMode
from use import get

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

async def send_to_authorisation_type1(server, client, text):
    memberlist = []
    if path.isfile("SETTINGS/" + server.id + "/permission_type1.txt"):
        with open("SETTINGS/" + server.id + "/permission_type1.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        for x in content:
            memberlist.append(get.member_by_role(server,discord.utils.get(server.roles, name=str(x))))
        for x in memberlist:
            try:
                await client.send_message(x, text)
            except:
                pass

def exist_all_folders(dbx, path):
    res = dbx.files_list_folder(path)
    count = 0
    for file in res.entries:
        count += 1
    return count


def drop_up(drop_path, file_path):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    up = open(file_path, 'rb')
    dbx.files_upload(up.read(), drop_path, mode=WriteMode.overwrite)



def drop_down(drop_path, file_path):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    metadata, f = dbx.files_download(drop_path)
    out = open(file_path, 'wb')
    out.write(f.content)
    out.close()