import discord
from use import use, get

async def ex(args, message, client, invoke, server):
    args_out = ""
    if len(args) > 0:
        args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
        if args_out == "a big boy" or args_out == "A Big Boy":
            if await use.assign_role("Im A Big Boy",message, client, message.channel, get.member_by_message(server, message), server):
                await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou can now proudly say: \nIm A Big Boy and can look at juicy pictures!!!"))

        elif args_out == "a big girl" or args_out == "A Big Girl":
            if await use.assign_role("Im A Big Girl", message, client, message.channel, get.member_by_message(server, message), server):
                await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou can now proudly say: \n Im A Big Girl and can look at juicy pictures!!!"))

        else:
            await use.error("The command is not valid.", message.channel, client)
    else:
        await use.error("The command is not valid.", message.channel, client)