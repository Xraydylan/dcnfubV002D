import discord
from os import path
from use import get,use

reach = 0

async def check_count(client, server, member):
    global reach
    count = server.member_count
    channel = client.get_channel("405502332902703106")

    path_file = "SETTINGS/" + server.id + "/reach.txt"
    path_drop = "/Gear_Two/reach.txt"

    if not path.isfile(path_file):
        f = open(path_file, "w")
        f.write("0")
        f.close()
    try:

        use.drop_down(path_drop,path_file)

        with open(path_file) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        reach = int(content[0])

    except:
        print("upload reach")
        await update_reach(reach, path_file, path_drop)

    if count == 100 and reach == 0:
        reach = 1
        await update_reach(reach, path_file, path_drop)

        await one_hundered(client, server, channel, member)

    print("Success")


async def one_hundered(client, server, channel, member):
    path100 = "data/100.jpg"

    await client.send_message(channel, "Hey!!!\n**We are now 100 people in the Nerfy Army!!!**")
    await client.send_message(channel, "Congratulations to %s!\nYou are the 100th member, who joined the server!!!\nYou won free merch from Nerfys collection!!!\nHe will contact you soon!" % member.mention)
    await client.send_file(channel, path100)
    await client.send_message(channel, "We are 100% awesome!")


async def update_reach(num, path_file, path_drop):
    global reach
    f = open(path_file, "w")
    f.write(str(num))
    f.close()

    use.drop_up(path_drop ,path_file)