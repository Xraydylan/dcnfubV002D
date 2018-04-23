from use import use,get
from os import path
from commands import cmd_com_own

async def ex(args, message, client, invoke, server):
    path_file = "data/temp/custom.txt"
    member = get.member_by_id(server, message.author.id)
    id = member.id
    if not path.isfile(path_file):
        cmd_com_own.download_custom()

    if len(args) > 0:
        trigger = args.__str__()[1:-1].replace("'", "").replace(",", "")

        with open(path_file) as f:
            content = f.readlines()
            content = [x.strip() for x in content]

        send_str = ""

        for x in content[1:]:
            x_sp = x.split(" ")
            if x_sp[0] == id:
                if x_sp[1].replace("-", " ") == trigger:
                    send_str = x_sp[2].replace("-", " ")

        if send_str == "":
            await use.error("No command could be found.", message.channel, client)
        else:
            await client.send_message(message.channel, send_str)
