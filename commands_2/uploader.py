import dropbox
from dropbox.files import WriteMode
import discord
import CONECT
import os
import random
from use import use,get
import time
import threading
import asyncio
from os import path
from datetime import datetime

status = 0
send_channel = None

first = 0
send_status = 0
send_time = (20, 00)

async def ex(args, message, client, invoke, server):
    global status, send_channel, first
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    if await use.dev_authorisation_type1(server, get.member_by_message(server, message)):
        if use.exist_all_folders(dbx,"/Pictures") == 3:
            if len(args) > 0:
                args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
                if args_out == "ping up":
                    await client.send_message(message.channel, "Up Pong!")
                elif args_out == "reset info":
                    await reset_info(dbx,client,message.channel)
                elif args_out == "upload count":
                    await get_upload_count(dbx,client,message.channel)
                elif args_out == "send":
                    await send(client,message.channel)


                elif args_out == "status":
                    if status == 0:
                        content = "The Autouploader is off."
                    else:
                        content = "The Autouploader is on."
                    await client.send_message(message.channel, content)


                elif args_out == "start":
                    if status == 0:
                        await check_for_channel_file(client, message.channel, server)
                        #print (send_channel)
                        if send_channel != None:
                            content = "Starting uploader."
                            status = 1
                            update_status(1)

                            main_loop = asyncio.get_event_loop()

                            #Start the thread
                            threading.Thread(name='sender_loop', target=sender_loop, args=(client,  main_loop)).start()

                        else:
                            content = "There is no channel set."

                    else:
                        content = "The Autouploader is already on."
                    await client.send_message(message.channel, content)


                elif args_out == "stop":
                    if status == 0:
                        content = "The Autouploader is already off."
                    else:
                        content = "Stopping uploader."
                        status = 0
                        update_status(0)

                    await client.send_message(message.channel, content)

                elif args_out == "set":
                    await set_channel(dbx, client, message.channel)

                elif args_out == "first message":
                    first = 1
                    await client.send_message(message.channel, "Activated first message!")

        else:
            await client.send_message(message.channel, "There is a storage problem. Folders are missing!")



def increase_down_count(dbx):


    path_file = "data/info.txt"
    path_drop = "/Pictures/info/name_info.txt"

    metadata, f = dbx.files_download(path_drop)
    numbers = str(f.content).replace("b", "").replace("'", "").split("\\r\\n")
    lastn = int(numbers[len(numbers)-1])+1
    out = open(path_file, 'wb')
    out.write(f.content)
    out.close()
    txt = open(path_file, 'w')
    txt.write(str(lastn))
    txt.close()

    use.drop_up(path_drop,path_file)

    os.remove(path_file)
    return lastn

async def reset_info(dbx,client,channel):
    await client.send_message(channel, "Info reseted")

    path_file = "data/info_reset.txt"
    path_drop = "/Pictures/info/name_info_reset.txt"

    use.drop_down(path_drop, path_file)

    up = open(path_file, 'rb')
    dbx.files_upload(up.read(), "/Pictures/info/name_info.txt", mode=WriteMode('overwrite'))
    up.close()
    os.remove(path_file)

async def send(client,channel):
    global first
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    res = dbx.files_list_folder("/Pictures/main")
    file_list = []
    for file in res.entries:
        file_list.append(file.name)

    if len(file_list) > 0:
        send_name = random.choice(file_list)

        path_drop = '/Pictures/main/' + send_name
        path_file = "data/temp/" + send_name

        use.drop_down(path_drop, path_file)

        print("mid")
        if first == 1:
            first = 0
            await client.send_message(channel, "Hey, hey, hey\nSaucy Bot is online and will currently send a picture every day XD!!!")

        await client.send_file(channel, path_file)
        print("send")
        from_path = "/Pictures/main/" + send_name
        to_path = "/Pictures/output/" + send_name

        dbx.files_move_v2(from_path, to_path, allow_shared_folder=False, autorename=True)

        os.remove(path_file)
        increase_down_count(dbx)
    else:
        print ("Empty")

async def get_upload_count(dbx,client,channel):


    path_drop = "/Pictures/info/name_info.txt"
    path_file = "data/info.txt"

    use.drop_down(path_drop, path_file)

    with open("data/info.txt") as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        await client.send_message(channel, "%s pictures have been uploaded." % content[0])

    os.remove("data/info.txt")



async def set_channel(dbx, client, channel):
    global send_channel
    path_channel = "data/temp/channel.txt"
    channel_id = channel.id
    path_dbx = "/Pictures/info/channel.txt"

    #if not path.isfile(path_channel):

    f = open(path_channel, "w")
    f.write(str(channel_id))
    f.close()

    use.drop_up(path_dbx,path_channel)

    send_channel = channel


async def check_for_channel_file(client, channel, server):
    global send_channel
    path_channel = "data/temp/channel.txt"
    path_dbx = "/Pictures/info/channel.txt"

    try:
        use.drop_down(path_dbx,path_channel)

    except:
        print("No online file")


    if not path.isfile(path_channel):
        if channel != None:
            await client.send_message(channel, "No channel was previously set.")
    else:
        with open(path_channel) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()

        #print(int(content[0]))
        channel_f = server.get_channel(str(content[0]))
        send_channel = channel_f



def sender_loop(client, main_loop):
    global send_channel, status, send_time
    print("loop_on")
    while status == 1:
        if check_for_time(send_time):
            main_loop.create_task(send(client,send_channel))
        time.sleep(60)


def check_for_time(send_time):
    global send_status
    ti = str(datetime.utcnow()).split(" ")[1].split(":")[0:2]

    cur_time = time_create(int(ti[0])+2, int(ti[1]))

    window_send = time_create(send_time[0],send_time[1]+2)

    window_reset = time_create(send_time[0], send_time[1] + 4)

    #Not corrected
    if comp_time_greater(cur_time, send_time) and comp_time_greater(window_send, cur_time):
        print("Check")
        if send_status == 0:
            send_status = 1
            return True

    if comp_time_greater(cur_time, window_send) and comp_time_greater(window_reset,cur_time):
        send_status = 0
    return False


def time_create(hours, min):
    if min >=60:
        min -= 60
        hours += 1
    if hours >= 24:
        hours -= 24

    return (hours,min)

def comp_time_greater(time1, time2):

    if time1[0] >= time2[0]:
        if time1[1] >= time2[1]:
            return True
    return False

def update_status(num):

    path_file = "data/temp/status.txt"
    path_drop = "/Pictures/info/status.txt"
    f = open(path_file, "w")
    f.write(str(num))
    f.close()
    use.drop_up(path_drop, path_file)


async def re_status(client, main_loop, server):
    global status

    path_file = "data/temp/status.txt"
    path_drop = "/Pictures/info/status.txt"


    use.drop_down(path_drop, path_file)

    with open(path_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        f.close()

    if content[0] != str(status):
        print ("Error")
        error_process("Status reset!")

    status = int(content[0])

    if status == 1:
        await check_for_channel_file(client, None, server)
        # Start the thread
        threading.Thread(name='sender_loop', target=sender_loop, args=(client, main_loop)).start()




def error_process(error):

    path_file = "data/temp/error.txt"
    path_drop = "/Pictures/info/error.txt"

    use.drop_down(path_drop, path_file)

    with open(path_file, "a") as myfile:
        new_id = "\n" + str(error)
        myfile.write(new_id)
        myfile.close()

    use.drop_up(path_drop, path_file)

    os.remove(path_file)
