import discord
from discord import Game, Embed
import dropbox
import CONECT

def member_by_role(server, role):
    for n in server.members:
        if role in n.roles:
            return n
    return None

def member_by_message(server, message):
    return server.get_member(message.author.id)

def member_by_id(server, id):
    for n in server.members:
        if id in n.id:
            return n
    return None


def members_auth2(server):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    loc_path = "SETTINGS/" + server.id + "/permission_type2.txt"
    try:
        metadata, f = dbx.files_download("/Gear_Two/permission_type2.txt")
        out = open(loc_path, 'wb')
        out.write(f.content)
        out.close()
    except:
        print("File not in Dropbox.")

    with open(loc_path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    return content