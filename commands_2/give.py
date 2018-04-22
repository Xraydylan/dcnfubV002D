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
import datetime
from commands_2 import uploader
from datetime import datetime as dt

send_channel = None

delta_add = datetime.timedelta(days=0)

async def ex(args, message, client, invoke, server):
    global send_channel

    #dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    send_channel = uploader.send_channel

    ##send_channel = message.channel

    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")

        if args_out == "me juice":
            await give_juice(client, server, send_channel, message)

        #elif args_out == "test":
        #    print (send_channel.id)

        else:
            await use.error(("The command is not valid!"), message.channel, client)


async def give_juice(client, server, channel, message):
    global send_channel, delta_add

    tday = dt.utcnow().date()

    ti = str(dt.utcnow()).split(" ")[1].split(":")[0:2]
    cur_time = time_create(int(ti[0]) + 2, int(ti[1]))

    user = message.author

    path_file = "data/temp/give_info.txt"
    path_drop = "/Pictures/info/give_info.txt"

    try:
        use.drop_down(path_drop,path_file)
    except:
        print("No file found!")

    if not path.isfile("data/temp/give_info.txt"):
        f = open(path_file, "w")
        f.write("0")
        f.close()

    with open(path_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        f.close()
    if content[0] != "0":
        delta_add = datetime.timedelta(days=0)
        if check_for_new_day(content[0], tday, cur_time, 0):
            if check_player_can(content, user, tday, cur_time):
                await uploader.send(client, send_channel)
                #print ("Would send!!!!!!!")
                update_give_info(user, tday, path_file, path_drop)

            else:
                #Send "You can not request more than one picture within 3 days..."
                await use.error("You can not request more than one picture within 3 days...", message.channel, client)

        else:
            #Send "You have to wait till the next day..."
            await use.error("Juice was already given today. \nYou have to wait till the next day...", message.channel, client)

    else:
        await uploader.send(client, send_channel)
        update_give_info(user, tday, path_file, path_drop)
    #print("Done")

def check_for_new_day(date_string, tday, cur_time, days):
    global delta_add
    date_list = date_string.split("-")
    date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

    delta = tday-date

    if delta.days < days:
        return False

    if delta.days == days:
        if cur_time[0] <= 2:
            delta_add = datetime.timedelta(days=1)
            return True
        else:
            return False
    else:
        return True

def check_player_can(content, user, tday, cur_time):

    content_s = content[1:]

    for x in content_s:
        x_s = x.split(" ")
        if x_s[0] == user.id:
            if check_for_new_day(x_s[1], tday, cur_time, 3):
                return True
            else:
                return False
    return True



def update_give_info(user, tday, path_file, path_drop):
    global delta_add
    f = open(path_file, "r")
    lines = f.readlines()
    f.close()

    lines = lines[1:]

    date_line = str(tday + delta_add) + "\n"
    user_line = str(user.id) + " " + str(tday + delta_add)+ "\n"

    f = open(path_file, "w")
    f.write(date_line)
    for line in lines:
        line_list = line.split(" ")
        if line_list[0] != str(user.id):
            f.write(line)
    f.write(user_line)
    f.close()

    use.drop_up(path_drop,path_file)


def time_create(hours, min):
    if min >=60:
        min -= 60
        hours += 1
    if hours >= 24:
        hours -= 24

    return (hours,min)






