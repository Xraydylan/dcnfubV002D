import discord
from discord import Game, Embed

def member_by_role(server, role):
    for n in server.members:
        if role in n.roles:
            return n
    return None

def member_by_message(server, message):
    return server.get_member(message.author.id)