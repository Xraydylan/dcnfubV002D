import discord
from use import use,get

async def ex(args, message, client, invoke, server):
    args_out = ""
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "RPG-Player":
            if await use.assign_role(args_out, message, client, message.channel, get.member_by_message(server, message), server):
                await message_RPG_Master(message, client, get.member_by_message(server, message), server)
        else:
            await use.error("The role can´t be found or accessed.", message.channel, client)

    else:
        await use.error("The command is not valid.", message.channel, client)



async def message_RPG_Master(message, client, user, server):
    role_master = discord.utils.get(server.roles, name="RPG-Master")
    if role_master == None:
        await use.error("Something in the code went wrong!", message.channel, client)
    else:
        master = get.member_by_role(server, role_master)
        if master == None:
            await use.error("Something went wrong!", message.channel, client)
        else:
            await client.send_message(master, embed=discord.Embed(color=discord.Color.green(), description="The Member:\n%s \nIs now a RPG-Player." % user.mention))