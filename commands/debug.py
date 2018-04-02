import discord
from use import use,get


async def ex(args, message, client, invoke, server):
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "picture":
            await send_picture(client, server, message)

        else:
            await use.error("The command is not valid.", message.channel, client)
    else:
        await use.error("The command is not valid.", message.channel, client)

async def send_picture(client, server, message):
    await  client.send_file(message.channel, "data/X.jpg")