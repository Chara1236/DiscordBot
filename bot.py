import traceback
import asyncpraw
import discord
import os
import asyncio
import time
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from discord.ext.commands import CommandOnCooldown
import random
import praw

global deletemode
deletemode = False
me = "universe#5319"
client = discord.Client()
url = os.getenv('url')
cluster = MongoClient(url)
db = cluster["post"]
collection = db["col"]
user = cluster["User"]
balance = user["Balance"]
inventory = user["Inventory"]
Noresponse = ["Bro che cho why the heck didn't you respond?",
              "Yo nerd if your going to use a command at least ANSWER me",
              "Ok just going to remain slient? Bruhhh",
              "Yo wtf I came online just to run this command and you ignore me?"]
client = commands.Bot(command_prefix='much ', )
client.remove_command('help')


def noresponsemessage(ctx):
    return random.choice(Noresponse)


def updateinventory(user: discord.Member, field):
    userid = user.id
    username = user
    try:
        collect = inventory.find_one({"_id": userid})
        placeval = collect[field]
        if collect["name"] != str(username):
            inventory.update_one({"_id": userid}, {"$set": {"name": str(username)}})
    except Exception as e:
        print(str(e))
        newpost = {"_id": userid, "name": str(username)}
        inventory.update_one({"_id": userid}, {"$set": {field: 0}})


def UpdateNewBalance(member: discord.Member):
    userid = member.id
    username = member
    try:
        money = balance.find_one({"_id": userid})
        if money["name"] != str(username):
            balance.update_one({"_id": userid}, {"$set": {"name": str(username)}})
    except Exception as e:
        print(str(e))
        newbalance = {"_id": userid, "name": str(username), "money": 0}
        balance.insert_one(newbalance)
        newinv = {"_id": userid, "name": str(username)}
        inventory.insert_one(newinv)
    updateinventory(member, "flexs")
    updateinventory(member, "dogecoin")
    # updateinventory(member, "test")

    # try:
    #     flexs = inventory.find_one({"_id": userid})
    #     flexamount = flexs["flexs"]
    #     if flexs["name"] != str(username):
    #         inventory.update_one({"_id": userid}, {"$set", {"name": str(username)}})
    # except Exception as e:
    #     newbalance = {"_id": userid, "name": str(username), "flexs": 0}
    #     inventory.insert_one(newbalance)


@client.command()
async def help(ctx, thing=None):
    if thing is None:
        await ctx.send("bruh what do you need help with?")
    if thing == "rainbow":
        rainbowinfo = discord.Embed(title="Rainbow Rules:", color=discord.Color.dark_gold())
        rainbowinfo.add_field(name="**wasd to move**", value="type w/a/s/d and enter to travel in those directions",
                              inline=False)
        rainbowinfo.add_field(name="**how to win**", value="get to the bottom right corner",
                              inline=False)
        rainbowinfo.add_field(name="**Select level**",
                              value="type much rainbow <level>, currently there are 2 levels, if no level is written, the map will be randomly generated",
                              inline=False)
        rainbowinfo.add_field(name="**enter e to exit**", value="EEEEEEEEE",
                              inline=False)
        rainbowinfo.add_field(name="**Red  :red_square:**",
                              value="These squares are death, you move there and you go back to the start",
                              inline=False)
        rainbowinfo.add_field(name="**Orange  :orange_square:**",
                              value="These squares make you orange flavour and removes other flavours",
                              inline=False)
        rainbowinfo.add_field(name="**Yellow**  :yellow_square:",
                              value="These squares make you lemon flavour and removes other flavours",
                              inline=False)
        rainbowinfo.add_field(name="**Green  :green_square:**",
                              value="Plain old normie squares, does nothing",
                              inline=False)
        rainbowinfo.add_field(name="**Blue**  :blue_square:",
                              value="These squares are ice, the will automatically teleport you to the next square, and if you slide out the map, you die",
                              inline=False)
        rainbowinfo.add_field(name="**Purple  :purple_square:**",
                              value="These squares belong to the grape gang, if you are lemon flavour and you step in their turf, ye ded boi",
                              inline=False)
        rainbowinfo.add_field(name="**Brown  :brown_square:**",
                              value="These squares are orange temples, if you are orange flavour and step on these and not on any edge, all 4 adjacent blocks will rotate 90 degrees clockwise ",
                              inline=False)
        rainbowinfo.add_field(name="**White  :white_large_square:**",
                              value="If you step on white and you are orange flavour, you die.",
                              inline=False)
        rainbowinfo.add_field(name="**Yeah I need to add more rules later**", value="In mean times ur a bean",
                              inline=False)
        await ctx.send(embed=rainbowinfo)


@client.command()
async def givenewbal(ctx, member: discord.Member):
    if str(ctx.message.author) == me:
        userid = member.id
        username = member
        # await ctx.send("command sent")
        #         # post = {"_id": userid, "name": str(username)}
        #         # print(post)
        #         # inventory.insert_one(post)

        UpdateNewBalance(member)
        await ctx.send("Check update")
    else:
        await ctx.send("Filthy peasants like you don't have access to this command.")


@client.command()
async def UpdateAllInv(ctx, field):
    print("Command typed")
    if str(ctx.message.author) == me:
        updates = inventory.find({field: {"$exists": False}})
    else:
        await ctx.send("Nerdddd u dont got no permissions to use this command")


@client.command()
async def AddUserInventoryField(ctx, field):
    print("Command typed")
    if str(ctx.message.author) == me:
        updates = inventory.find({field: {"$exists": False}})
        inventory.update_many({"$set": {'' + str(field): 0}})
    else:
        await ctx.send("Nerdddd u dont got no permissions to use this command")


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def bal(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    UpdateNewBalance(member)
    userid = member.id
    username = member
    try:
        money = balance.find_one({"_id": userid})
        if money["name"] != str(username):
            await ctx.send("Bruh you changed your name")
            balance.update_one({"_id": userid}, {"$set": {"name": str(username)}})
    except Exception as e:
        print(str(e))
        newbalance = {"_id": userid, "name": str(username), "money": 0}
        balance.insert_one(newbalance)
    moneyy = balance.find_one({"_id": userid})
    actualmoney = moneyy["money"]
    invinfo = inventory.find_one({"_id": userid})
    dogecoins = invinfo["dogecoin"]
    value = random.randint(0, 0xffffff)
    showmoney = discord.Embed(title=str(username) + "'s Balance", color=value)
    showmoney.add_field(name="$" + str(actualmoney), value="------------", inline=False)
    showmoney.add_field(name="Dogecoins: " + str(dogecoins), value="------------", inline=False)
    await ctx.send(embed=showmoney)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    user = str(ctx.message.author)
    money = random.randint(0, 100)
    balance.update_one({"name": user}, {"$inc": {"money": money}})
    await ctx.channel.send("You found **$" + str(money) + "**!")


async def editmap(channel, startmap, embed, locr, locc, character, user, flavour):
    endmap = discord.Embed(title=user + "'s Rainbow Game")
    for x in range(8):
        s = ""
        for y in range(8):
            if x == locr and y == locc:
                s += character
            else:
                s += startmap[x][y]
        endmap.add_field(name=s, value="\u200b", inline=False)
    endmap.add_field(name="Flavour", value=flavour, inline=False)
    await channel.send(embed=endmap)
    # await embed.edit(embed=endmap)


async def getmsg(chan, user: discord.Member, timeout):
    author = ""
    while author != user:
        msg = await client.wait_for("message", timeout=timeout)
        author = msg.author
    return msg

async def noresponsemessage(ctx):
    return random.choice(Noresponse)

async def editmap(channel, startmap, embed, locr, locc, character, user, flavour):
    endmap = discord.Embed(title=user + "'s Rainbow Game")
    for x in range(8):
        s = ""
        for y in range(8):
            if x == locr and y == locc:
                s += character
            else:
                s += startmap[x][y]
        endmap.add_field(name=s, value="\u200b", inline=False)
    endmap.add_field(name="Flavour", value=flavour, inline=False)
    await channel.send(embed=endmap)
    # await embed.edit(embed=endmap)

@client.command()
async def rainbow(ctx, level=None):
    r = ":red_square:"
    o = ":orange_square:"
    y = ":yellow_square:"
    g = ":green_square:"
    b = ":blue_square:"
    p = ":purple_square:"
    w = ":white_large_square:"
    br = ":brown_square:"
    gamemaps = [
        [[g, r, r, r, r, r, r, r], [g, g, g, g, g, g, r, r], [g, r, r, g, r, r, g, g], [g, r, r, g, r, r, r, g],
         [g, g, r, g, g, r, r, g], [r, r, r, r, g, g, g, g], [r, r, g, g, g, r, r, r], [r, r, g, g, g, g, g, g]]
        , [[g, y, g, g, g, p, g, o], [y, y, g, p, g, g, g, p], [p, p, p, p, p, p, p, p], [r, r, g, r, r, r, r, r],
           [g, r, br, r, g, g, g, y], [g, g, r, g, g, g, g, r], [w, r, r, r, r, r, r, r], [g, b, g, b, g, b, g, g]]]
    global deletemode
    if deletemode == False:
        user = str(ctx.message.author)
        deletemode = True
        flavour = "none"
        character = ":dog:"
        locr = 0
        locc = 0
        colours = [":white_large_square:", ":brown_square:", ":red_square:", ":orange_square:", ":yellow_square:",
                   ":green_square:", ":blue_square:", ":purple_square:"]
        grid = discord.Embed(title=str(user) + "'s Rainbow Game")
        mapinfo = [[0 for i in range(8)] for j in range(8)]
        if level is None:
            for x in range(int(8)):
                s = ""
                for y in range(int(8)):
                    colour = random.choice(colours)
                    mapinfo[x][y] = colour
                    if x == 0 and y == 0:
                        s += character
                    elif x == 7 and y == 7:
                        s += ":green_square:"
                    else:
                        s += colour
                grid.add_field(name=s, value="\u200b", inline=False)
        else:
            level = int(level) - 1
            for x in range(8):
                s = ""
                for y in range(8):
                    if x == 0 and y == 0:
                        s += str(character)
                    else:
                        s += str(gamemaps[int(level)][x][y])
                    mapinfo[x][y] = str(gamemaps[int(level)][x][y])
                grid.add_field(name=s, value="\u200b", inline=False)
        grid.add_field(name="Flavour", value=flavour, inline=False)
        await ctx.send(
            "Press 'e' to quit, wasd for you know exactly what, else ur a fake gamer, much help rainbow for more info")
        map = await ctx.send(embed=grid)
        endmap = discord.Embed(title=str(user) + "'s Rainbow Game")
        endmap.add_field(name=s, value="\u200b", inline=False)
        mapinfo[0][0] = ":green_square:"
        mapinfo[7][7] = ":green_square:"
        choice = 'c'
        direction = "none"
        try:
            while choice != 'e':
                msg = await getmsg(ctx, ctx.message.author, 300)
                choice = msg.content
                # await ctx.channel.purge(limit=1)
                if choice == 'd' and locc < 7:
                    locc += 1
                    direction = "right"
                elif choice == 'a' and locc > 0:
                    locc -= 1
                    direction = "left"
                elif choice == 's' and locr < 7:
                    locr += 1
                    direction = "down"
                elif choice == 'w' and locr > 0:
                    locr -= 1
                    direction = "up"
                breakcheck = True
                while mapinfo[locr][locc] == ":blue_square:" and breakcheck:
                    if direction == "up":
                        if locr > 0:
                            locr -= 1
                        else:
                            locr = 0
                            locc = 0
                            breakcheck = False
                    if direction == "down":
                        if locr < 7:
                            locr += 1
                        else:
                            locr = 0
                            locc = 0
                            breakcheck = False
                    if direction == "left":
                        if locc > 0:
                            locc -= 1
                        else:
                            locr = 0
                            locc = 0
                            breakcheck = False
                    if direction == "right":
                        if locc < 7:
                            locc += 1
                        else:
                            locr = 0
                            locc = 0
                            breakcheck = False
                if mapinfo[locr][locc] == ":red_square:":
                    locr = 0
                    locc = 0
                elif mapinfo[locr][locc] == ":yellow_square:":
                    flavour = ":lemon:"
                elif mapinfo[locr][locc] == ":orange_square:":
                    flavour = ":tangerine:"
                elif mapinfo[locr][locc] == ":purple_square:" and flavour == ":lemon:":
                    locr = 0
                    locc = 0
                    flavour = "none"
                elif mapinfo[locr][locc] == w and flavour == ":tangerine:":
                    locr = 0
                    locc = 0
                    flavour = "none"
                elif mapinfo[locr][
                    locc] == ":brown_square:" and flavour == ":tangerine:" and 0 < locc < 7 and 0 < locr < 7:
                    print('e')
                    temp = mapinfo[locr - 1][locc]
                    mapinfo[locr - 1][locc] = mapinfo[locr][locc - 1]
                    mapinfo[locr][locc - 1] = mapinfo[locr + 1][locc]
                    mapinfo[locr + 1][locc] = mapinfo[locr][locc + 1]
                    mapinfo[locr][locc + 1] = temp
                await editmap(ctx, mapinfo, map, locr, locc, character, user, flavour)
                if locr == 0 and locc == 0:
                    flavour = "none"
                if locr == 7 and locc == 7:
                    await ctx.send("You Win, ur cool")
                    deletemode = False
                    return
            await ctx.send("Ok ended nerd")
            deletemode = False
        except Exception as TimeoutError:
            print(str(TimeoutError))
            await ctx.send(noresponsemessage(ctx))
    else:
        await ctx.send("Yo ur already playing this game")


@client.command()
async def shop(ctx):
    shop = discord.Embed(title="**SHOP**", color=discord.Color.red())
    shop.add_field(name="**Flex: $10**", value="Yeah all this does it flex that's it :/      :muscle: ", inline=False)
    shop.add_field(name="**Doge currently unbuyable**", value="Idk yet just here for testing      :dog:", inline=False)
    await ctx.send(embed=shop)


@client.command()
async def inv(ctx, *, username: discord.Member = None):
    author = ctx.message.author
    something = False
    if username is None:
        username = author
    if not username.bot:
        UpdateNewBalance(username)
        invinfo = inventory.find_one({"name": str(username)})
        showinventory = discord.Embed(title=str(username) + "'s Inventory", color=discord.Color.orange())
        if invinfo["flexs"] > 0:
            something = True
            showinventory.add_field(name="**Flexes:**       :muscle: ", value=str(invinfo["flexs"]))
        if not something:
            showinventory.add_field(name="**Lmao ur broke af**", value="POOOOOOOOOOOOOOOOOOOOORRRRRRRRR")

        await ctx.send(embed=showinventory)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def mine(ctx):
    await asyncio.sleep(0.5)
    userid = ctx.message.author.id
    operation = random.randint(1, 2)
    int1 = random.randint(1, 10)
    int2 = random.randint(1, 10)
    if operation == 1:
        await ctx.send("Solve the equation to mine dogecoin! " + str(int1) + " + " + str(int2))
    elif operation == 2:
        await ctx.send("Solve the equation to mine dogecoin! " + str(int1) + " x " + str(int2))
    try:
        prizerange = random.randint(1, 100)
        prize = 0
        mesg = await getmsg(ctx, ctx.message.author, 10)
        msg = mesg.content
        if prizerange == 100:
            prize = 1000
        else:
            prize = random.randint(1, 3)
        if operation == 1:
            if str(msg) == str(int1 + int2):
                await ctx.send(
                    "Nice you have at least the brain size of a 5 year old! You get " + str(prize) + " Doge(s)!")
                inventory.update_one({"_id": userid}, {"$inc": {"dogecoin": prize}})
            else:
                await ctx.send("Yo dumb boi that aint the right answer")
        elif operation == 2:
            if str(msg) == str(int1 * int2):
                await ctx.send(
                    "Nice you have at least the brain size of a 5 year old! You get " + str(prize) + " Doge(s)!")
                inventory.update_one({"_id": userid}, {"$inc": {"dogecoin": prize}})
            else:
                await ctx.send("Yo dumb boi that aint the right answer")
    except asyncio.TimeoutError:
        await ctx.send(random.choice(Noresponse))


@client.command()
async def use(ctx, *, thing):
    author = ctx.message.author
    userid = ctx.message.author.id
    username = str(author)
    UpdateNewBalance(author)
    if thing == "flex":
        flexinfo = inventory.find_one({"_id": userid})
        if flexinfo["flexs"] > 0:
            inventory.update_one({"_id": userid}, {"$inc": {"flexs": -1}})
            await ctx.send("Oh yeah you use your flex on everyone in the server, wow they are impressed")
        else:
            await ctx.send("Bruh what the hec you can't just use something you don't have dumbtard")


@client.command()
async def buy(ctx, thing, amount=1):
    author = ctx.message.author
    username = str(author)
    UpdateNewBalance(author)
    userid = ctx.message.author
    userbalinfo = balance.find_one({"name": username})
    userbal = userbalinfo["money"]
    if thing == "flex":
        flexinfo = inventory.find_one({"name": username})
        if userbal >= 10 * amount:
            inventory.update_one({"name": username}, {"$inc": {"flexs": amount}})
            await ctx.send("You now have " + str(flexinfo["flexs"] + amount) + " flexs!")
            balance.update_one({"name": username}, {"$inc": {"money": -10 * amount}})
        else:
            await ctx.send("Ayooo bruh u can't afford this noob")


async def clears(ctx, amount='1'):
    if amount == 'all':
        await ctx.channel.purge(limit=9999999)
    else:
        await ctx.channel.purge(limit=int(amount) + 1)


@client.command()
async def clear(ctx, amount='1'):
    if amount == 'all':
        await ctx.channel.purge(limit=9999999)
    else:
        await ctx.channel.purge(limit=int(amount) + 1)


# When bot is online
@client.event
async def on_ready():
    print('Bot logged in as {0.user}'
          .format(client))


# @client.event
# async def on_message(message):
#     global deletemode
#     msg = message.content
#     if deletemode and not message.author.bot and msg != 'e' and msg != 'a' and msg != 'w' and msg != 'd' and msg != 's':
#          await message.purge(limit=1)
#          await message.channel.send("yeet")
#     await message.delete()
# @client.event
# async def on_command_error(ctx, exc):
#     if isinstance(exc, CommandOnCooldown):
#         msg = await ctx.send(f"chill dude try again in {exc.retry_after:,.0f} secs.")
#     elif isinstance(exc, TimeoutError):
#         await ctx.send(random.choice(Noresponse))
#     else:
#         print(str(exc))


client.run(os.getenv('token'))
