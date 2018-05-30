import discord

async def ex(args, message, client, invoke, server):
    #args_out = ""
    #if len(args) > 0:
    #    args_out = "\n\n*Attached arguments: %s*" % args.__str__()[1:-1].replace("'", "")
    await client.send_message(message.channel, "Pong!")