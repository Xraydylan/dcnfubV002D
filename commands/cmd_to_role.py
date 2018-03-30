import discord


async def error(content, channel, client):
    await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

async def ex(args, message, client, invoke):
    args_out = ""
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "Spoiler Squad":
            await assign_role(args_out, message, client, message.channel, message.author)

        if args_out == "RPG-Player":
            await assign_role(args_out, message, client, message.channel, message.author)

        else:
            await error("The role can´t be found or accessed.", message.channel, client)

    else:
        await error("The command is not valid.", message.channel, client)

async def assign_role(rolename, message, client, channel, user):
    role = discord.utils.get(message.server.roles, name=rolename)

    if role == None:
        await error("Something went wrong with the role assignment", message.channel, client)
    else:
        if role in user.roles:
            await error("You already have that role.", message.channel, client)
        else:
            await client.add_roles(user, role)
            await client.send_message(channel, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou are now part of: \n%s!" % role.name))

