import tweepy

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)

token = "xd"
prefix = "+"

from distutils import errors
from logging import error
import discord
from discord.ext import commands, tasks
from discord.utils import get

import re
import json

import string
import random
import requests
import asyncio
 
from datetime import datetime
from time import sleep, localtime, strftime

intents = discord.Intents
intents = intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=prefix, intents=intents)

@client.event
async def on_ready():

    print(f'{strftime("%H:%M:%S", localtime())}: Logged in as: {client.user}')
    print(f'{strftime("%H:%M:%S", localtime())}: Bot ID: {client.user.id}\n\n')
 
@client.command(name='say', brief='make the bot say something')
async def deez(ctx, *, args):
    await ctx.send(args)
 
@client.command(name='id', brief='get a persons discord id by pinging them')
async def id(ctx, args):
    await ctx.reply(int(''.join(filter(str.isdigit, args))), mention_author = False)
 
@client.command(name='cock', brief='get your cock length')
async def pp(ctx):
    await ctx.reply(f'you got a {random.randint(0, 25)}cm long cock', mention_author = False)
 
@client.command(name='genkey', brief='generate a key with random characters, max chars = 2000')
async def randomkey(ctx, args):
    randomKey = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(int(args)))
    await ctx.reply(f'Your generated key is: {randomKey}', mention_author = False)
    print(f'{strftime("%H:%M:%S", localtime())}: {ctx.author}, generated a key: {randomKey}')

    if args == None:
        randomKey = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(int(random.randint(1,100))))
        await ctx.reply(f'Your generated key is: {randomKey}', mention_author = False)
        print(f'{ctx.author}, generated a key: {randomKey}')

@client.command(name='dice', brief='roll a number between 1-6')
async def roll(ctx):
    clientNumber = random.randint(1,6)
    botNumber = random.randint(1,6)
    if botNumber > clientNumber:
        await ctx.reply(f':game_die: You **lost**! :game_die:\n:game_die: You got: **{clientNumber}** :game_die:\n:game_die: I got: **{botNumber}** :game_die:', mention_author = False)
    elif botNumber < clientNumber:
        await ctx.reply(f':game_die: You **won**! :game_die:\n:game_die: You got: **{clientNumber}** :game_die:\n:game_die: I got: **{botNumber}** :game_die:', mention_author = False)
    elif botNumber == clientNumber:
        await ctx.reply(f':game_die: We got a **tie**! :game_die:\n:game_die: You got: **{clientNumber}** :game_die:\n:game_die: I got: **{botNumber}** :game_die:', mention_author = False)
 
@client.command(name='rps', brief='choices: rock, paper or scissors')
async def kps(ctx, valinta):
    valinnat=["rock", "paper", "scissors"]
    if valinta not in valinnat:
        await ctx.reply("usable choices: rock, paper or scissors")
    else:
        await ctx.reply(random.choice(valinnat), mention_author = False)
 
@client.command(name='howgay', brief='check how gay you are')
async def gayness(ctx):
    gay = random.randint(0,100)
    await ctx.reply(f':rainbow_flag: you are {gay}% homosexual :rainbow_flag:', mention_author = False)
 
@client.command(name='avatar', brief='get persons avatar')
async def avatar(ctx, *, member: discord.Member = None):
       if member == None:
            avatarLink = ctx.author.display_avatar
            await ctx.reply(avatarLink)
       else:
            avatarLink = member.display_avatar
            await ctx.reply(avatarLink)

@client.command(name='namelist', brief='get a possible list of usernames.')
async def usernames(ctx, arg):
    robloxUrl = f'https://api.roblox.com/users/get-by-username?username={arg}'

    if arg != arg.isdigit():
        data1 = requests.get(robloxUrl).json()
        userid = data1['Id']
        arg = userid

        crntNameDataUrl = f'https://users.roblox.com/v1/users/{arg}'
        crntNameData = requests.get(crntNameDataUrl).json()
        crntName = crntNameData['name']

        namesurl = f'https://users.roblox.com/v1/users/{arg}/username-history?limit=100&sortOrder=Asc'
        data = requests.get(namesurl).json()
        allnames = []
    else:

        crntNameDataUrl = f'https://users.roblox.com/v1/users/{arg}'
        crntNameData = requests.get(crntNameDataUrl).json()
        crntName = crntNameData['name']

        namesurl = f'https://users.roblox.com/v1/users/{arg}/username-history?limit=100&sortOrder=Asc'
        data = requests.get(namesurl).json()
        allnames = []

    for i in data["data"]:
        clearNames = str(i["name"])
        allnames.append(clearNames)
    await ctx.reply(f"**Names:**: {', '.join(allnames)} and the current name: {crntName}! **Amount of names: __{len(allnames)} + 1 (Current username).__**")

@client.command(name='discord', brief='get info about a discord profile by id or by tagging them')
async def discordInfo(ctx, arg):
    guild = client.get_guild(1026769243867455528)
    discordId = ''.join(filter(str.isdigit, arg))
    member = await ctx.guild.fetch_member(discordId)
    if member != None:
        avatarLink = member.display_avatar
    
        date_format = "%Y, %b %d, %a @ %I:%M %p"

        user = await client.fetch_user(discordId)
        if user != None:
            embed=discord.Embed(title="Discord info", url=f"https://www.famility.xyz", description="User info:", color = discord.Colour.random())
            embed.set_author(name="Bot maker: ren !#8079")
            embed.set_thumbnail(url=avatarLink)
            embed.add_field(name="Creation date:", value=f"**{user.created_at.strftime(date_format)}**", inline=True)
            embed.add_field(name="Server join date:", value=f"**{member.joined_at.strftime(date_format)}**", inline=True)
            embed.add_field(name="Discord Id:", value=f"**{discordId}**", inline=True)
            embed.add_field(name="Name:", value=f"**{user.name}#{str(user.discriminator)}**", inline=True)
            embed.set_footer(text="ren sex dick cheese bot")

            await ctx.reply(embed=embed, mention_author = False)
         
@discordInfo.error
async def dInfo(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        guild = client.get_guild(1026769243867455528)

        avatarLink = ctx.author.display_avatar 
        date_format = "%Y, %b %d, %a @ %I:%M %p"

        embed=discord.Embed(title="Discord info", url=f"https://www.famility.xyz", description="User info:", color = discord.Colour.random())
        embed.set_author(name="Bot maker: ren !#8079")
        embed.set_thumbnail(url=avatarLink)
        embed.add_field(name="Creation date:", value=f"**{ctx.author.created_at.strftime(date_format)}**", inline=True)
        embed.add_field(name="Server join date:", value=f"**{ctx.author.joined_at.strftime(date_format)}**", inline=True)
        embed.add_field(name="Discord Id:", value=f"**{ctx.author.id}**", inline=True)
        embed.add_field(name="Name:", value=f"**{ctx.author.name}#{str(ctx.author.discriminator)}**", inline=True)
        embed.set_footer(text="ren sex dick cheese bot")

        await ctx.reply(embed=embed, mention_author = False)

@client.command(name='roblox', brief='get info about a roblox profile by id')
async def robloxInfo(ctx, *, arg):

    if arg.isdigit():
        int(arg)
        robloxuseridUrl = f'https://users.roblox.com/v1/users/{arg}'
        data = requests.get(robloxuseridUrl).json()
        description = data['description']
        name = data['name']
        displayname = data['displayName']
        userId = arg
        isbanned = data['isBanned']
        created = data['created']
        Verified = ''
    else:
        robloxUrl = f'https://api.roblox.com/users/get-by-username?username={arg}'
        data = requests.get(robloxUrl).json()
        userId = data['Id']
        arg = data['Id']
 
        robloxuseridUrl = f'https://users.roblox.com/v1/users/{arg}'
        data = requests.get(robloxuseridUrl).json()

        description = data['description']
        name = data['name']
        displayname = data['displayName']
        userId = arg
        isbanned = data['isBanned']
        created = data['created']
        Verified = ''
    try:

        if isbanned == True:
            Verified = "Player is banned"
        else:
            isownedurl = f'https://inventory.roblox.com/v1/users/{arg}/items/Asset/102611803/is-owned' or f'https://inventory.roblox.com/v1/users/{arg}/items/Asset/1567446/is-owned'
            inventoryData = requests.get(isownedurl).json()

            canViewUrl = f'https://inventory.roblox.com/v1/users/{arg}/can-view-inventory'
            viewData = requests.get(canViewUrl).json()
            canView = viewData['canView']

            if canView and inventoryData == True:
                Verified = "True"
            elif canView == True and inventoryData == False:
                Verified = "False"
            elif canView == False:
                Verified = "Inventory is disabled."

        dateTime = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%fZ')
        accurateCreation = f"{dateTime.day}.{dateTime.month}.{dateTime.year}"

        if description == "" or None:
            description = f"Sadly **{name}** does not have a description."

        embed=discord.Embed(title=f"{name}'s profile link", url=f"https://www.roblox.com/users/{userId}/profile", description="Player info:", color = discord.Colour.random())
        embed.set_author(name="Bot maker: ren !#8079")
        embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={userId}&width=150&height=150&format=png")
        embed.add_field(name="Username:", value=f"**{name}**", inline=True)
        embed.add_field(name="Display name:", value=f"**{displayname}**", inline=True)
        embed.add_field(name="UserID:", value=f"**{userId}**", inline=True)
        embed.add_field(name="Banned:", value=f"**{isbanned}**", inline=True)
        embed.add_field(name="Verified:", value=f"{Verified}", inline=True)
        embed.add_field(name="Created:", value=f"**{accurateCreation}**", inline=True)
        embed.add_field(name="Description:", value=f"**{description}**", inline=True)
        embed.set_footer(text="ren sex dick cheese bot")
        await ctx.reply(embed=embed, mention_author = False)

    except:
            error=data['errors']
            if error:
                fullreply = str(error[0]["message"] + " Try again with another id since " + str(error[0]["userFacingMessage"])).lower()
                reply = fullreply.replace(".", ",")
                await ctx.reply(reply, mention_author = False)

@client.command(name='convert', brief='+convert c/f amount of degrees.')
async def s(ctx, arg, arg2):

    if arg.lower() == "c" or arg.lower() == "celsius":

        cthermo = int(arg2)
        cthermo = cthermo * 1.8
        cthermo = cthermo + 32
        cthermo = "{:.1f}".format(cthermo)

        await ctx.reply(f'{arg2} °C is {str(cthermo)} °F')

    elif arg.lower() == "f" or arg.lower() == "fahrenheit":

        fthermo = int(arg2)
        fthermo = fthermo - 32
        fthermo = fthermo * 5
        fthermo = fthermo / 9
        fthermo = "{:.1f}".format(fthermo)

        await ctx.reply(f'{arg2} °F is {str(fthermo)} °C')

    else:
        await ctx.reply("Make sure you use f or fahrenheit for example.")


@client.command(name='userid', brief='get roblox players id with username')
async def accountInfo(ctx, arg):
    robloxUrl = f'https://api.roblox.com/users/get-by-username?username={arg}'
    data = requests.get(robloxUrl).json()

    id = data['Id']

    if data['Id'] == "":
        id = "something fucked up lol"

    if arg != None or "":
        await ctx.reply(f"**{arg}**'s UserId is:", mention_author = False)
        await ctx.send(f"**{id}**")

@client.command(name='suggest', brief='suggest something, if the owner accepts it the bot will send you a dm')
async def suggest(ctx, *, arg):
    check = '✅'
    x = '❌'

    owner = client.get_user(int(ctx.guild.owner.id))
    print(owner)
    avatarLink = ctx.author.display_avatar
    ownerlink = client.get_user(int(ctx.guild.owner.id)).display_avatar
    print(avatarLink)
    embed=discord.Embed(title=f"Suggestion:", description=f"{arg}", color = discord.Colour.random())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{avatarLink}")
    embed.set_footer(text=f"Suggested by: {ctx.author}")

    channel = client.get_channel(1029124114121773086)
    message = await channel.send(embed=embed)
    await message.add_reaction(check)
    await message.add_reaction(x)

    def check(reaction, user):
        return user == owner and str(reaction.emoji) in ['✅'] and reaction.message == message
    
    confirmation = await client.wait_for("reaction_add", check=check) 

    if confirmation:
        embed = discord.Embed(title="", description=f"Accepted suggestion:\n**{arg}**", color=discord.Color.from_rgb(0,255,0))
        embed.set_author(name=f"{owner} accepted your suggestion.", icon_url=f"{avatarLink}")
        embed.set_footer(text=f"Suggestion accepted by: {owner}")

        await ctx.author.send(embed=embed)

@client.command(name='homie', brief='sends my homie')
async def homie(ctx):
    homieprofile = "https://www.roblox.com/users/27729207"
    await ctx.reply(f"My dear homie is: :heart_eyes: {homieprofile} :heart_eyes:", mention_author = False)

@client.command(name='tweet', brief='tweets something you include, must be text currenty. includes your name, tag and discord id.')
async def tweet(ctx, *, arg):
    tweet = f"{ctx.author}\n{ctx.author.id}\nTweets: {arg}"
    status = api.update_status(status=tweet)

    await ctx.reply(f"Succesfully tweeted **{arg}**, remember your username, tag and discord id are included in the tweet to know who tweeted it.", mention_author = False)

@client.command(name='getsomebitches', brief='get bitches')
async def bitches(ctx):
    randomBitches = random.randrange(0,10)
    if randomBitches == 0:
        await ctx.reply(f'u got {randomBitches} bitches fr :skull:', mention_author = False)
    else:
        await ctx.reply(f'nice u got {randomBitches} bitches at least its better than 1 :scream:', mention_author = False)

@client.command(name='r34', brief='get a random r34 post')
async def r34(ctx):
    randomPost = random.randrange(1, 6826315)
    sentPost = f'https://rule34.xxx/index.php?page=post&s=view&id={randomPost}'
    await ctx.reply(sentPost, mention_author = False)

@client.command(name='e621', brief='get a random 361 post')
async def r34(ctx): 
    randomPost = random.randrange(14, 3624788)
    sentPost = f'https://e621.net/posts/{randomPost}'
    await ctx.reply(sentPost, mention_author = False)

@client.command(name='renstime')
async def time(ctx):
    await ctx.reply(f"Ren's current time is: {strftime('%H:%M:%S', localtime())}", mention_author = False)

@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(color=discord.Color.from_rgb(255,0,0))
    if isinstance(error, commands.CommandNotFound):

     embed.title = "Command was not found."
     embed.description = "The " + f"{error}".lower() + ". Use **+help** to find all the commands and how to use them."

     print(f'\n{ctx.author.name}#{str(ctx.author.discriminator)} used a command that does not exist, error: {str(error)}\n')
     await ctx.reply(embed=embed, mention_author = False)

client.run(token)
