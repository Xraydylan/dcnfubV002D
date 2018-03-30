async def ex(args, message, client, invoke):
    await client.send_message(message.channel, "And a hello back!")