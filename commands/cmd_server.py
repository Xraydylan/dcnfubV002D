import discord
from use import use,get

async def ex(args, message, client, invoke, server):
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "member count":
            await  client.send_message(message.channel, "The server has currently %s members." % server.member_count)
        else:
            await use.error("The command is not valid.", message.channel, client)

    else:
        await use.error("The command is not valid.", message.channel, client)