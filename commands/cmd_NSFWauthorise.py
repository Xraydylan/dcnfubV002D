import discord


async def error(content, channel, client):
    await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

async def ex(args, message, client, invoke, server):
    args_out = ""
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "a big boy" or args_out == "A Big Boy":
            await assign_role("Im A Big Boy",message, client, message.channel, server.get_member(message.author.id), server)

        elif args_out == "a big girl" or args_out == "A Big Girl":
            await assign_role("Im A Big Girl", message, client, message.channel, server.get_member(message.author.id), server)

        else:
            await error("The command is not valid.", message.channel, client)
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
            await client.send_message(channel, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou can now proudly say: \n%s!!!" % role.name))