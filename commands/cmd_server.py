import discord
from use import use,get


async def ex(args, message, client, invoke, server):
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "member count":
            await  client.send_message(message.channel, "The server has currently %s members." % server.member_count)

        elif args_out == "roles":
            await all_roles(client, message, server)
        else:
            await use.error("The command is not valid.", message.channel, client)
    else:
        await use.error("The command is not valid.", message.channel, client)

async def all_roles(client, message, server):
    final = "**The server has currently these roles:**\n"
    roles_all = []
    for discord.role in server.roles:
        if not "@" in str(discord.role):
            roles_all.append(str(discord.role))
    roles_all = sorted(roles_all)

    for i in roles_all:
        final = final + "~ " + i + "\n"

    await  client.send_message(message.channel, final)