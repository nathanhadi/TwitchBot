# bot.py
import os # for importing env vars for the bot to use
from twitchio.ext import commands
import random

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=["iamERNE", "Unbannedgoofwall"]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    #await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

# @bot.event
# async def event_message(ctx):\
#     # make sure the bot ignores itself and the streamer
#     if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
#         return

#     if ctx.author.is_mod:
#         print("mod has typed.")

@bot.event
async def event_raw_usernotice(channel, tags: dict):
    name = tags['login']
    if (tags['msg-id'] == 'subgift'):
        print(name)
        newdict = await readFile()
        newdict[name] = newdict.get(name, 0) + 1
        await writeFile(newdict)
    if (tags['msg-id'] == 'sub' or tags['msg-id'] == 'resub'):
        print(name)
        newdict = await readFile()
        newdict[name] = newdict.get(name, 0) + 1
        await writeFile(newdict)

async def writeFile(dictionary):
    file1 = open("RaffleTickets.txt", "w")
    file1.truncate()
    for i in dictionary:
        file1.write(str(i))
        file1.write(" ")
        file1.write(str(dictionary[i]))
        file1.write("\n")
    file1.close()

async def readFile():
    dictionary = {}
    file1 = open("RaffleTickets.txt", "r")
    list1 = file1.readlines()
    for i in list1:
        names = i.split()
        dictionary[names[0]] = int(names[1])
    file1.close()
    return dictionary

@bot.command(name='test')
async def test(ctx):
    if ctx.author.is_mod:
        data = await readFile()
        data["erne"] = data.get("erne", 0) + 1
        await writeFile(data)
        print(data)

@bot.command(name='hunt')
async def bonus(ctx):
    slots = ""

    for i in range(0, len(bonushunt)):
        if i == 0:
            slots += bonushunt[i]
        else:
            slots += ", "
            slots += bonushunt[i]

    if len(bonushunt) == 0:
        await ctx.channel.send("No Bonuses so far.")
    elif len(bonushunt) == 1:
        await ctx.channel.send(f"{bonuscount} Bonus: ({slots})")
    else:
        await ctx.channel.send(f"{bonuscount} Bonuses: ({slots})")

@bot.command(name='change')
async def change(ctx):
    if ctx.author.is_mod:
        global bonuscount
        bonuscount = ctx.content[8:]

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.is_mod:
        global bonuscount
        global bonushunt
        bonushunt = []
        bonuscount = 0

@bot.command(name='add')
async def add(ctx):
    slot = ctx.content[5:]
    global bonuscount
    if ctx.author.is_mod:
        if slot in bonushunt:
            print('Slot already in bonushunt.')
        else:
            bonushunt.append(slot)
            bonuscount += 1
    # slots = ""

    # for i in range(0, len(bonushunt)):
    #     if i == 0:
    #         slots += bonushunt[i]
    #     else:
    #         slots += ", "
    #         slots += bonushunt[i]

    # if len(bonushunt) == 0:
    #     await ctx.channel.send("No Bonuses so far.")
    # elif len(bonushunt) == 1:
    #     await ctx.channel.send(f"{bonuscount} Bonus: {slots}")
    # else:
    #     await ctx.channel.send(f"{bonuscount} Bonuses: {slots}")

@bot.command(name='del')
async def delete(ctx):
    slot = ctx.content[5:]
    global bonuscount
    if ctx.author.is_mod:
        if slot in bonushunt:
            bonushunt.remove(slot)
            bonuscount -= 1
        else:
            print('Slot not in bonushunt.')
    slots = ""

    # for i in range(0, len(bonushunt)):
    #     if i == 0:
    #         slots += bonushunt[i]
    #     else:
    #         slots += ", "
    #         slots += bonushunt[i]

    # if len(bonushunt) == 0:
    #     await ctx.channel.send("No Bonuses so far.")
    # elif len(bonushunt) == 1:
    #     await ctx.channel.send(f"{bonuscount} Bonus: {slots}")
    # else:
    #     await ctx.channel.send(f"{bonuscount} Bonuses: {slots}")


if __name__ == "__main__":
    bonuscount = 0
    bonushunt = []
    bot.run()