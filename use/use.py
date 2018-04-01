import discord
from discord import Game, Embed

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