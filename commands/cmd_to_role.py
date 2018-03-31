import discord


async def error(content, channel, client):
    await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

async def ex(args, message, client, invoke, server):
    args_out = ""
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "RPG-Player":
            await assign_role(args_out, message, client, message.channel, server.get_member(message.author.id), server)

        else:
            await error("The role can´t be found or accessed.", message.channel, client)

    else:
        await error("The command is not valid.", message.channel, client)

async def assign_role(rolename, message, client, channel, user, server):
    role = discord.utils.get(server.roles, name=rolename)
    if role == None:
        await error("Something went wrong with the role assignment", message.channel, client)
    else:
        if role in user.roles:
            await error("You already have that role.", message.channel, client)
        else:
            await client.add_roles(user, role)
            await client.send_message(user, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou are now part of: \n%s!" % role.name))
            if rolename == "RPG-Player":
                await message_RPG_Master(message, client, user, server)

async def message_RPG_Master(message, client, user, server):
    role_master = discord.utils.get(server.roles, name="RPG-Master")
    if role_master == None:
        await error("Something in the code went wrong!", message.channel, client)
    else:
        master = get_member(server, role_master)
        if master == None:
            await error("Something went wrong!", message.channel, client)
        else:
            await client.send_message(master, embed=discord.Embed(color=discord.Color.green(), description="The Member:\n%s \nIs now a RPG-Player." % user.mention))

def get_member(server, role):
    for n in server.members:
        if role in n.roles:
            return n
    return None