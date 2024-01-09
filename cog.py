import discord
from discord.ext import commands
import random
global deletemode
deletemode = False
Noresponse = ["Bro che cho why the heck didn't you respond?",
                  "Yo nerd if your going to use a command at least ANSWER me",
                  "Ok just going to remain slient? Bruhhh",
                  "Yo wtf I came online just to run this command and you ignore me?"]
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    async def getmsg(self, chan, user: discord.Member, timeout):
        author = ""
        while author != user:
            msg = await self.wait_for("message", timeout=timeout)
            author = msg.author
        return msg

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    def noresponsemessage(ctx):
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

    @commands.command()
    async def rainbow(self, ctx, level=None):
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