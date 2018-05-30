import discord
from use import use,get
import CONECT
import os


async def ex(args, message, client, invoke, server):
    if await use.dev_authorisation_type1(server, get.member_by_message(server, message)):
        if len(args) > 0:
            args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
            if args_out == "completed":
                await refuel(client, message.channel)
    else:
        await use.error("You don´t have the right permission to say this.", message.channel, client)

async def refuel(client, channel):
    await client.send_message(channel, "The Saucy Bot has been refueled and is again ready for business!")
    await get_picture_refuel(client, channel)

async def get_picture_refuel(client, channel):
    path_drop = '/Pictures/info/images/refueled.png'
    path_file = "data/temp/refueled.png"
    use.drop_down(path_drop, path_file)
    print("mid")
    await client.send_file(channel, path_file)
    print("send")
    os.remove(path_file)