import discord
from discord import Game, Embed
import dropbox
import CONECT
from use import use
from os import path

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

    drop_path = "/Gear_Two/permission_type2.txt"
    try:
        use.drop_down(drop_path, loc_path)
    except:
        print("File not in Dropbox.")

    with open(loc_path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    return content

def merberlist_by_idlist(server, id_list):

    member_list = []

    for n in server.members:
        if n.id in id_list:
            member_list.append(n)
    if len(member_list) > 0:
        return member_list
    else:
        return None

def namestring_by_memberlist(member_list, type = 0):

    namestring = ""

    if type == 0:
        namestring = "\n"
        for n in member_list:
            namestring = namestring + n.name + "\n"
    elif type == 1:
        for n in member_list:
            namestring = namestring + n.name + " ,"
        namestring = namestring[0:len(namestring)-1]

    elif type == 2:
        namestring = "\n"
        for n in member_list:
            namestring = namestring + n.mention + "\n"
    elif type == 3:
        for n in member_list:
            namestring = namestring + n.mention + " ,"
        namestring = namestring[0:len(namestring)-1]

    return namestring

def direct_namestring_by_idlist(server, id_list, type = 0):

    member_list = merberlist_by_idlist(server, id_list)

    string = namestring_by_memberlist(member_list, type)

    return string

def txt_content_as_string(path_txt):

    if path.isfile(path_txt):
        with open(path_txt) as f:
            contentpre = f.read()

        return contentpre

    return ""