from use import use,get
from os import path



async def ex(args, message, client, invoke, server):

    member = get.member_by_id(server, message.author.id)

    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")


        if args_out == "my commands":
            await dis_my_com(client, member)

        args_split = args_out.split(" ")

        if len(args_split) == 2:
            if args_split[0] == "delete":
                # trigger getrennt durch -
                await delete_com(client, member, args_split[1])

        elif len(args_split) == 3:
            if args_split[0] == "new":
                # trigger und result getrennt durch -
                await create_new_com(client, member ,args_split[1], args_split[2])
            else:
                await use.error("The command is not valid. There might be a mistake.", message.channel, client)

        else:
            await use.error("The command is not valid. (Too many spaces)", message.channel, client)
    else:
        await use.error("The command is not valid.", message.channel, client)


async def dis_my_com(client, member):

    path_file = "data/temp/custom.txt"
    id = member.id

    with open(path_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    a = ""
    for x in content[1:]:
        part = x.split(" ")
        if part[0] == id:
            append = "Trigger: \"%s\" Result: \"%s\"\n" % (part[1].replace("-", " "), part[2].replace("-", " "))
            a = a + append

    if len(a) == 0:
        await use.error("You have not created your own commands yet",member,client)
    else:
        content = "Here are all your personal commands:\n" + a
        await client.send_message(member, content)

async def create_new_com(client, member ,invoke, result):
    download_custom()

    id = member.id

    path_file = "data/temp/custom.txt"
    path_drop = "/Gear_Two/custom.txt"

    with open(path_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    if check_contains(content, id, invoke):
        await use.error("There is already a command with the trigger: \"%s\"" % invoke.replace("_", " "), member, client)
    else:
        append_str = "%s %s %s\n" % (id, invoke, result)

        with open(path_file, "a") as f:
            f.write(append_str)
        content = "Success!\nYour command trigger is:\n%s\nThe result will be:\n%s" % (invoke.replace("-"," "), result.replace("-"," "))
        await client.send_message(member, content)

        use.drop_up(path_drop,path_file)


async def delete_com(client, member, invoke):
    download_custom()

    id = member.id

    path_file = "data/temp/custom.txt"
    path_drop = "/Gear_Two/custom.txt"

    with open(path_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    if check_contains(content, id, invoke):
        with open(path_file, "w") as f:
            f.write("0\n")
            for x in content[1:]:
                x_sp = x.split(" ")
                if x_sp[0] != id or x_sp[1] != invoke:
                    f.write(str(x)+"\n")
        use.drop_up(path_drop,path_file)
        await client.send_message(member,"The command with the trigger \"%s\" has been removed." % invoke)
    else:
        await use.error("There is no command with the trigger: \"%s\"" % invoke.replace("_", " "),member, client)

def check_contains(list, id, invoke):
    for x in list[1:]:
        x_sp = x.split(" ")
        if x_sp[0] == id:
            if x_sp[1] == invoke:
                return True
    return False

def download_custom():
    path_file = "data/temp/custom.txt"
    path_drop = "/Gear_Two/custom.txt"

    try:
        use.drop_down(path_drop, path_file)
    except:
        if not path.isfile(path_file):
            f = open(path_file, "w")
            f.write("0\n")
            f.close()

