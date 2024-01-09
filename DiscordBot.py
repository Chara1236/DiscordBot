import discord
import os
import asyncio
import time
from discord.ext import commands
import random
import pymongo
from pymongo import MongoClient
from discord.ext.commands import CommandOnCooldown

me = "universe#5319"
client = discord.Client()
url = os.getenv('url')
cluster = MongoClient(url)
db = cluster["post"]
collection = db["col"]
user = cluster["User"]
balance = user["Balance"]
client = commands.Bot(command_prefix='much ')

global h
global t
h: int = 0
t: int = 0
messages = 0

def getCard():
    return random.randint(2, 14)

def cardValue(a):
    if(a<=10):
        return a;
    elif(a<14):
        return 10;
    else:
        return 11;
def showCard(a):
    if a <= 10:
        return a
    elif a == 11:
        return "J"
    elif a == 12:
        return "Q"
    elif a == 13:
        return "K"
    else:
        return "A"


@client.command()
async def animate(ctx):
    thing = []
    for x in range(10):
        thing.append("-")
    thing[0] = '*'
    msg = await ctx.send("*---------")
    for x in range(9):
        await asyncio.sleep(0.01)
        thing[x] = "-"
        thing[x+1] = '*'
        s = ""
        for y in range(10):
            s += thing[y]
        await msg.edit(content=s)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    user = str(ctx.message.author)
    money = random.randint(0, 100)
    balance.update_one({"name": user}, {"$inc": {"money": money}})
    await ctx.channel.send("You found **$" + str(money) + "**!")

@client.command()
async def steal(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Yo u gotta steal from someone")
    else:
        monsteal = balance.find_one({"name": str(member)})
        moneysteal = int(monsteal["money"]/2)
        curbal = balance.find_one({"name": str(ctx.message.author)})
        bal = curbal["money"]

        if str(ctx.message.author) == "universe#5319":
            balance.update_one({"name": str(ctx.message.author)}, {"$inc": {"money": int(moneysteal)}})
            balance.update_one({"name": str(member)}, {"$inc": {"money": int(-1*moneysteal)}})
            await ctx.send("You stole $" + str(moneysteal) + " your balance is now :$" + str(bal+moneysteal))
        else:
            await ctx.send("Lmao what a nerd, only the almighty universe#5319 can steal not u peasant now I set ur balance to $0 lmaoooo")
            balance.update_one({"name": str(ctx.message.author)}, {"$set": {"money": 0}})
@client.command()
async def addmoney(ctx, member: discord.Member = None, money=0):

    if(str(ctx.message.author)==me):
        if member is None:
            member = ctx.message.author
        add = int(money)
        url = os.getenv('url')
        cluster = MongoClient(url)
        db = cluster["User"]
        collection = db["Balance"]
        user = str(member)
        try:
            balance = collection.find_one({"name": user})
            collection.update_one({"name": user}, {"$inc": {"money": add}})
            await ctx.send(user + "'s Balance is:$" + str(balance['money']+add))
        except:
            newbalance = {"name": user, "money": add}
            collection.insert_one(newbalance)
            await ctx.send(user + "'s Balance is:$"+ str(newbalance['money']))
    else:
        await ctx.send("You dont have the permissions to do this command")


@client.command(aliases=['bj'])
async def blackjack(ctx):
    await asyncio.sleep(0.25)
    pValue = 0
    pCards = ""
    pAce = False
    cValue = 0
    cAce = False
    cCards = ""
    card = ''
    choice = 'h'
    mcard = 0
    for x in range(2):
        card = getCard()
        pCards = pCards + " " + str(showCard(card))
        pValue += cardValue(card)
        if(card == 14):
            pAce = True

    if pAce == False or pValue - 10 < 1:
        await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue) + ")")
    elif pAce == True and pValue > 21:
        await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue - 10) + ")")
    else:
        await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue) + " or "
                               + str((pValue - 10)) + ")")

    for x in range(2):
        card = getCard()
        if x == 1:
         cCards = cCards + " " + str(showCard(card))
        else:
            cCards += "?"
            mcard = card
        cValue += cardValue(card)
        if (card == 14):
            pAce = True
    await ctx.send("Computer cards are " + cCards)
    choice = 'h'

    while(pValue<21 or (pValue<30 and pAce == True)) and choice == 'h':
        await ctx.send("Yo fam u wanna hit or stand? (h/s) type anything else to leave")
        try:
            msg = await client.wait_for("message", timeout=20)
            if msg.content.lower() == "h":
                choice = 'h'
                card = getCard()
                await ctx.channel.send("You draw a " + str(showCard(card)))
                pCards += " " + str(showCard(card))
                pValue += cardValue(card)
                if card == 14:
                    pAce = True

                if pAce == False or pValue - 10 < 1:
                    await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue) + ")")
                elif pAce == True and pValue>=21:
                    print(pAce)
                    await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue-10) + ")")
                else:
                    await ctx.channel.send("Your cards are " + str(pCards) + " Total Value(" + str(pValue) + " or "
                         + str((pValue-10)) + ")")
            elif msg.content.lower() == "s":
                choice = 's'
            else:
                await ctx.send("k I stopped the game")
                return

        except asyncio.TimeoutError:
            await ctx.send("Bro che cho why the heck didnt u respond")
            return

    if (pAce and pValue > 21):
        pValue -= 10
    if(pValue<22):
        while (cValue < 17 or (cValue < 26 and cAce == True)):
            card = getCard()
            cValue += cardValue(card)
            cCards+= " " + str(showCard(card))
            if(card == 14):
                cAce = True


    if (cAce and cValue > 21):
        cValue -= 10

    await ctx.send("Computers card (" + str(showCard(mcard)) + ")" + str(cCards)+ " Total Value(" + str(cValue) + ")")
    win = False
    if(pValue>21):
        await ctx.send("Lmao Ur TRASH u busted, u lose")
    elif(cValue>21):
        await ctx.send("Computer was being to greedy and busted :/ u win")
        win = True
    elif(pValue == cValue):
        await ctx.send("Y'all tied with a score of " + str(cValue))
    elif(pValue > cValue):
        await ctx.send("You win " + str(pValue) + " to " + str(cValue))
        win = True
    else:
        await ctx.send("You lost " + str(pValue) + " to " + str(cValue))
    if(win):
        url = os.getenv('url')
        cluster = MongoClient(url)
        db = cluster["User"]
        collection = db["Balance"]
        author = str(ctx.message.author)
        try:
            curbal = collection.find_one({"name": author})
        except:
            await ctx.send("could not be found :/")
        winamount = random.randint(50,100)
        collection.update_one({"name": author}, {"$inc": {"money": winamount}})
        await ctx.send("You won $" + str(winamount) + " and your balance is now " + str(curbal["money"]+winamount))
    else:
       await ctx.send("Since you lost/tied you don't gain any money")


@client.command()
async def test(ctx):
    await ctx.channel.send(f"y or n")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower()

    try:
        msg = await client.wait_for("message", check=check, timeout=20)
        if msg.content.lower() == "y":
            await ctx.channel.send("You said yes!")
        else:
            await ctx.channel.send("You said no!")
    except asyncio.TimeoutError:
        await ctx.send("Bro che cho why the heck didnt u respond")

@client.command()
async def database(ctx):
    mongo_url = 'url'
    cluster = MongoClient(mongo_url)
    db = cluster["testing"]
    collection = db["name"]
    collect = db.collection
    author = ctx.author
    cool = collection.find({"Author": author})
    print(cool["_id"])
    print(str(cool))
    print("cool has ran")
    await ctx.channel.send(cool)

@client.command()
async def coolness(ctx, *, coolness):
    mongo_url = os.getenv('url')
    cluster = MongoClient(mongo_url)
    db = cluster["testing"]
    collection = db["name"]
    author = str(ctx.author)
    test = collection.find({"Author": author})

    collection.update_one({"Author": author}, {"$set": {"Coolness": coolness}})
    await ctx.channel.send("Updated")

@client.command(aliases=['pin', 'Ping', 'p'])
async def ping(ctx):
    print(os.getenv('url'))
    await ctx.send(f'current server ping: {round(client.latency*1000)}ms')

@client.command(aliases=['fc'])
async def flipcoin(ctx):
    global h
    global t
    choice = ['H', 'T']
    coin = choice[random.randint(0, 1)]
    ht = 0
    if coin == 'H':
        h += 1
        ht = h
    else:
        t += 1
        ht = t
    await ctx.send(coin+'  This side has been flipped '+str(ht)+" times")
    collection.update_one({"name": "Coins flipped"}, {"$inc": {"times": 1}})

@client.command()
async def flips(ctx):
    flipinfo = collection.find_one({"name": "Coins flipped"})
    flipamount = flipinfo["times"]
    await ctx.send("There have been " + str(flipamount) + " flip(s)")

@client.command()
async def version(ctx):
    await ctx.channel.send("Ur discord  is on version "+ discord.__version__)
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command(aliases=['len'])
async def length(ctx,*,word):
    await ctx.send(f'the length of "{word}" is ' + str(len(word)))

@client.command()
async def spam(ctx,*, word):
    for x in range(0,10):
     await ctx.send(str(word))

@client.event
async def on_ready():
    print('Bot logged in as {0.user}'
          .format(client))


@client.event
async def on_command_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        msg = await ctx.send(f"chill dude try again in {exc.retry_after:,.0f} secs.")

@client.command()
async def clear(ctx, amount='1'):
    if amount == 'all':
        await ctx.channel.purge(limit=9999999)
    else:
        await ctx.channel.purge(limit=int(amount)+1)

@client.command()
async def bot(ctx, *, user: discord.Member):
    if user.bot:
        await ctx.channel.send("yeah this nerd be bot")
    else:
        await ctx.channel.send('nah fam they aint a bot')

@client.command()
async def deluni(ctx):
    balance.delete_many({"name": "universe#5319", "money": 0})
    await ctx.send("junk cleared")


@client.command()
async def bal(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    url = os.getenv('url')
    cluster = MongoClient(url)
    db = cluster["User"]
    collection = db["Balance"]
    author = str(member)
    try:
        balance = collection.find_one({"name": author})
        s = author + "'s Balance :$" + str(balance['money'])
        embed = discord.Embed(
        title = author + "'s Balance")
        embed.add_field(name="$" + str(balance['money']), value="-----------")
        await ctx.send(embed=embed)
    except Exception as e:
        print(str(e))
        print(str(author))
        print(str(ctx.message.author.id))
        newbalance = {"_id": ctx.message.author.id, "name" : author, "money": 0}
        collection.insert_one(newbalance)
        embed = discord.Embed(title = author + "'s Balance")
        embed.add_field(name="$" + str(balance['money']), value="-----------")
        await ctx.send(embed=embed)


@client.command()
async def embed(ctx):
    embed = discord.Embed(
        title="Text Formatting",
        url="https://realdrewdata.medium.com/",
        description="Here are some ways to format text",
        color=discord.Color.blue())
    embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData",
                     icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
    # embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Learn more here: realdrewdata.medium.com")
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    global messages
    messages += 1
    msg = message.content
    if message.author == client.user:
        return;
    msgid = message.id

    # if msg.startswith('send doge pic'):
    #   await channel.send(file=discord.File('doge.jpg'))

    if msg.startswith("give me clout"):
        await message.add_reaction('\N{THUMBS UP SIGN}')

    if msg.startswith("!quote"):
        quote = (msg.split("quote ", 1)[1])
        await message.channel.send(str(quote) + " -" + str(message.author))

    if msg.startswith('!sup'):
        await asyncio.sleep(1)
        await message.channel.send('Yeah Im here')
        await asyncio.sleep(0.5)
        await message.channel.send("oh yeah the msg id is " + str(msgid))
        await client.change_presence(activity=discord.Game(name='Just talkin'))
    await client.process_commands(message)

# client.loop.create_task(update_storage())
client.run(os.getenv('tok'))
