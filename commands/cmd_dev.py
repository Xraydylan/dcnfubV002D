import discord
from use import use,get
import os
from os import path
import CONECT
import dropbox
from dropbox.files import WriteMode
from commands import anti_spam

initial = 0

async def ex(args, message, client, invoke, server):
    global initial
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")

        if initial == 0:
            if not path.isfile("SETTINGS/" + server.id + "/permission_type1.txt"):
                out = open("SETTINGS/" + server.id + "/permission_type1.txt", 'w')
                out.write("0\n")
                out.close()
            if not path.isfile("SETTINGS/" + server.id + "/permission_type2.txt"):
                out = open("SETTINGS/" + server.id + "/permission_type2.txt", 'w')
                out.write("0\n")
                out.close()

            initial = 1


        # All Authorisations (type 1 and 2)
        if await use.dev_authorisation_type2(server, message.author) or await use.dev_authorisation_type1(server, get.member_by_message(server, message)):
            if args_out == "ping auth2":
                await client.send_message(message.channel, "dev auth2 Pong!")
            elif args_out == "antispam status":
                await anti_spam.status_info(client, server, message.channel)
            elif args_out == "antispam start":
                await anti_spam.start_anti_spam(client, server, message.channel)
            elif args_out == "antispam stop":
                await anti_spam.stop_anti_spam(client, server, message.channel)
            elif args_out == "delete auth2":
                await delete_auth2(client, server, message.channel, message.author)

            # Only Authorisations type 1
            if await use.dev_authorisation_type1(server, get.member_by_message(server, message)):
                if args_out == "ping":
                    await client.send_message(message.channel, "dev Pong!")
                elif args_out == "pull authorisation type1":
                    await pull_authorisation_type1(client, server, message.channel)

                # Special args
                args_out_list = args_out.split(" ")
                if len(args_out_list) >= 1:
                    if len(args_out_list) == 3:

                        if args_out_list[0] == "add" and args_out_list[1] == "auth2":
                            print(args_out_list[2][2:len(args_out_list[2])-1])
                            await add_new_auth2(client, server, message.channel, args_out_list[2][2:len(args_out_list[2])-1])

                            #args_out.split(" ")[1][2:len(args_out.split(" ")[1])-1]



        else:
            await use.error("You don´t have the right permission to do this.", message.channel, client)

    else:
        await use.error("The command is not valid.", message.channel, client)

async def pull_authorisation_type1(client,server,channel):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    metadata, f = dbx.files_download("/Gear_Two/permission_type1.txt")
    out = open("SETTINGS/" + server.id + "/permission_type1.txt", 'wb')
    out.write(f.content)
    out.close()
    await client.send_message(channel, "Updating permissions type 1")

async def pull_authorisation_type2(client,server,channel):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    metadata, f = dbx.files_download("/Gear_Two/permission_type2.txt")
    out = open("SETTINGS/" + server.id + "/permission_type2.txt", 'wb')
    out.write(f.content)
    out.close()
    await client.send_message(channel, "Updating permissions type 2")


async def add_new_auth2(client, server, channel, id):
    member = get.member_by_id(server, id)
    if member == None:
        member = get.member_by_id(server, id[1:])

    if member == None:
        await client.send_message(channel, "Error! No member found!")
    else:
        await add_auth2(client, server, channel, member)





async def add_auth2(client, server, channel, member):
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    loc_path = "SETTINGS/" + server.id + "/permission_type2.txt"
    try:
        metadata, f = dbx.files_download("/Gear_Two/permission_type2.txt")
        out = open(loc_path, 'wb')
        out.write(f.content)
        out.close()
    except:
        print("File not in Dropbox.")
    if await use.dev_authorisation_type2(server, member) == False:
        with open(loc_path, "a") as myfile:
            new_id = "\n" + str(member.id)
            myfile.write(new_id)
            myfile.close()
        up = open(loc_path, 'rb')
        dbx.files_upload(up.read(), "/Gear_Two/permission_type2.txt", mode = WriteMode.overwrite)
        await client.send_message(channel, "Authorisation granted to %s" % member.mention)
    else:
        await client.send_message(channel, "Member %s already has authorisation2" % member.mention)


async def delete_auth2(client, server, channel, user):

    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    loc_path = "SETTINGS/" + server.id + "/permission_type2.txt"
    try:
        metadata, f = dbx.files_download("/Gear_Two/permission_type2.txt")
        out = open(loc_path, 'wb')
        out.write(f.content)
        out.close()
    except:
        print("File not in Dropbox.")


    if await use.dev_authorisation_type2(server, user):
        f = open(loc_path, "r")
        lines = f.readlines()
        f.close()

        f = open(loc_path, "w")
        for line in lines:
            if line != str(user.id) + "\n":
                f.write(line)
        f.close()

        up = open(loc_path, 'rb')
        dbx.files_upload(up.read(), "/Gear_Two/permission_type2.txt", mode = WriteMode.overwrite)
        await client.send_message(channel, "Authorisation off %s deleted!" % user.mention)


    else:
        await client.send_message(channel, "You do not have auth2.")