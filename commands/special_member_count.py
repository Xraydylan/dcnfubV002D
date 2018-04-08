import discord
import dropbox
from dropbox.files import WriteMode
import CONECT
from os import path

reach = 0

async def check_count(client, server, member):
    global reach
    count = server.member_count
    channel = client.get_channel("405502332902703106")
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    if not path.isfile("SETTINGS/" + server.id + "/reach.txt"):
        f = open("SETTINGS/" + server.id + "/reach.txt", "w")
        f.write("0")
        f.close()


    try:
        metadata, f = dbx.files_download("/Gear_Two/reach.txt")
        out = open("SETTINGS/" + server.id + "/reach.txt", 'wb')
        out.write(f.content)
        out.close()

        with open("SETTINGS/" + server.id + "/reach.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        reach = int(content[0])

    except:
        print("upload reach")
        await update_reach(0, dbx, server)

    if count == 100 and reach == 0:
        reach = 1
        await update_reach(reach, dbx, server)

        await one_hundered(client, server, channel, member)

    print("Success")


async def one_hundered(client, server, channel, member):
    path100 = "data/100.jpg"

    await client.send_message(channel, "Hey!!!\n**We are now 100 people in the Nerfy Army!!!**")
    await client.send_message(channel, "Congratulations to %s!\nYou are the 100th member, who joined the server!!!\nYou won free merch from Nerfys collection!!!\nHe will contact you soon!" % member.mention)
    await client.send_file(channel, path100)
    await client.send_message(channel, "We are 100% awesome!")


async def update_reach(num, dbx, server):
    global reach
    f = open("SETTINGS/" + server.id + "/reach.txt", "w")
    f.write(str(num))
    f.close()

    up = open("SETTINGS/" + server.id + "/reach.txt", 'rb')
    dbx.files_upload(up.read(), "/Gear_Two/reach.txt", mode=WriteMode.overwrite)