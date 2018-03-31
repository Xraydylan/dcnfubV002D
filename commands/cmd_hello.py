async def ex(args, message, client, invoke, server):
    await client.send_message(message.channel, "And a hello back!")