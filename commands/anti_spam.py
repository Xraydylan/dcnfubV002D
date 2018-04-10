import discord
from use import use,get
import os
from os import path
import CONECT
import dropbox
import time
import threading
import asyncio

status = 0
main_loop = None
sent_dict = {}
observe_dict = {}

async def status_info(client, server, channel):
    global status

    if status == 0:
        await client.send_message(channel, "Antispam is off.")
    else:
        await client.send_message(channel, "Antispam is on.")

async def start_anti_spam(client, server, channel):
    global status,main_loop

    main_loop = asyncio.get_event_loop()
    if status == 0:
        await client.send_message(channel, "Starting Antispam.")
        status = 1
    else:
        await client.send_message(channel, "Antispam is already on.")

async def stop_anti_spam(client, server, channel):
    global status
    if status == 0:
        await client.send_message(channel, "Antispam is already off.")
    else:
        await client.send_message(channel, "Stopping Antispam.")
        status = 0


async def new_message(client,message, server):
    global sent_dict, observe_dict

    user = message.author
    channel_id = message.channel.id


    # Spambot not active in Test Channel!!!!!!
    if str(channel_id) != "429051026251841536":

        if channel_id in sent_dict:
            if sent_dict[channel_id][0] == user and user != client.user:
                counter = sent_dict[channel_id][1]+1
                status_c = sent_dict[channel_id][2]
                status_t = sent_dict[channel_id][3]



                if counter >= 2 and status_t == 0:
                    status_t = 1
                    observe_dict[(channel_id, user)] = 0

                    threading.Thread(name='loop', target=loop, args=(client ,channel_id, user)).start()

                if status_t == 1 or status_t == 2:
                    temp = observe_dict[(channel_id, user)] + 1
                    observe_dict[(channel_id, user)] = temp


                if counter >= 10 and status_c == 0:
                    status_c = 1
                    spam_alert(client, channel_id, user)

                elif counter >= 20 and status_c == 1:
                    status_c = 2
                    spam_alert2(client, channel_id, user)


                sent_dict[channel_id] = (user, counter, status_c, status_t)
                #print(counter)

            else:
                st = sent_dict[channel_id][3]
                sent_dict[channel_id] = (user, 1, 0, st)
        else:
            sent_dict[channel_id] = (user, 1, 0, 0)


def loop(client, channel_id, user):
    global sent_dict, observe_dict

    time.sleep(2)

    if observe_dict[(channel_id, user)] >= 3 and sent_dict[channel_id][3] == 1:
        spam_alert_time(client, channel_id, user)
        counter = sent_dict[channel_id][1]
        status_c = sent_dict[channel_id][2]
        observe_dict[(channel_id, user)] = 0
        sent_dict[channel_id] = (user, counter, status_c, 2)
        threading.Thread(name='loop', target=loop, args=(client, channel_id, user)).start()

    elif observe_dict[(channel_id, user)] >= 3 and sent_dict[channel_id][3] == 2:
        spam_alert_timr2(client, channel_id, user)
        counter = sent_dict[channel_id][1]
        status_c = sent_dict[channel_id][2]
        sent_dict[channel_id] = (user, counter, status_c, 0)

    else:
        counter = sent_dict[channel_id][1]
        status_c = sent_dict[channel_id][2]
        sent_dict[channel_id] = (user, counter, status_c, 0)


def spam_alert(client, channel_id, user):
    print("Spam Alert")
    main_loop.create_task(send_spam_report(client, channel_id, user, 1))

def spam_alert2(client, channel_id, user):
    print("Spam Alert2!!!!!!!")
    main_loop.create_task(send_spam_report(client, channel_id, user, 2))

def spam_alert_time(client, channel_id, user):
    print("Spam Alert Time")
    main_loop.create_task(send_spam_report(client, channel_id, user, 3))


def spam_alert_timr2(client, channel_id, user):
    print("Spam Alert Time 2!!!!!!!")
    main_loop.create_task(send_spam_report(client, channel_id, user, 4))



async def send_spam_report(client, channel_id, user, type):
    channel = client.get_channel(channel_id)
    channel_mention = channel.mention
    user_mention = user.mention
    server = channel.server

    content = "None"

    if type == 1:
        content = "Spam Warning 1 in %s from %s.\n(Spam Count Warning 1)" % (channel_mention, user_mention)

    elif type == 2:
        content = "Spam Warning 2 in %s from %s.\n(Spam Count Warning 2!!!)" % (channel_mention, user_mention)

    elif type == 3:
        content = "Spam Warning 1 in %s from %s.\n(Spam Time Warning 1)" % (channel_mention, user_mention)

    elif type == 4:
        content = "Spam Warning 2 in %s from %s.\n(Spam Time Warning 2!!!)" % (channel_mention, user_mention)


    list = get.members_auth2(server)

    for number in list:
        member = get.member_by_id(server, number)
        await client.send_message(member, content)