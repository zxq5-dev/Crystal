import discord
from discord.ext import commands
from neuralintents import GenericAssistant
from dotenv import load_dotenv
import os
from calc import calculate
import random
import aiofiles
from datetime import datetime
import banned_words


chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()


client = commands.Bot(command_prefix = "$ ")

load_dotenv()
token = os.environ["token"]




class Logger():
    async def filter(self, message, words):
        try:
            async with aiofiles.open(f"./data/{message.guild.name}/chat_filter.log", mode = "a") as logfile:
                await logfile.write(f"[{get_time()}] : in channel: {message.channel}\n {message.author} used banned words: {words}\nin message: {message.content}\n\n")
        except:
            os.mkdir(f"./data/{message.guild.name}")
            async with aiofiles.open(f"./data/{message.guild.name}/chat_filter.log", mode = "a") as logfile:
                await logfile.write(f"[{get_time()}] : in channel: {message.channel}\n {message.author} used banned words: {words}\nin message: {message.content}\n\n")




def get_time():
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    return(time)





@client.command()
async def profile(message, member: discord.Member, description="Displays the profile of the specified user."):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Color.purple())
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    await message.send(embed=embed)


@client.command(pass_context = True, description="Clears the number of messages specified in the channel")
async def clear(ctx, args):
    channel = ctx.message.channel
    amount = args
    messages = []
    async for message in channel.history(limit = int(amount)+1):
        messages.append(message)
    await channel.delete_messages(messages)



@client.command(description="Kicks the specified user.")
@commands.has_permissions(kick_members=True)
async def kick(message, member : discord.Member, *, reason = None):
    if member == client.user:
        await message.send(random.choice["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna kick myself!"])

    elif member.top_role >= message.author.top_role:
        await message.send(random.choice["you cant kick members with higher permissions than yours", "sorry, you cant do that", "nice try :)"])

    elif member == message.author:
        await message.send(random.choice["lmao why would you want to kick yourself", "are you sure you want to do that?", "you cant kick yourself lol"])

    else:
        await member.kick(reason=reason)
        await message.send(f"kicked member:\n  '{member}'\nfor reason:\n  '{reason}'")

@kick.error
async def kick_error(message, error):
    if isinstance(error, commands.MissingPermissions):
        await message.send("sorry, you dont have permissions to do this!")
    print(error)

@client.command(description="Bans the specified user.")
@commands.has_permissions(ban_members=True)
async def ban(message, member : discord.Member, *, reason = None):
    if member == client.user:
        await message.send(random.choice["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna ban myself!"])
        return
    elif member.top_role >= message.author.top_role:
        await message.send(random.choice["you cant ban members with higher permissions than yours", "sorry, you cant do that", "nice try :)"])
        return

    elif member == message.author:
        await message.send(random.choice["lmao why would you want to ban yourself", "are you sure you want to do that?", "you cant ban yourself lol"])
        return

    else:
        await member.ban(reason=reason)
        await message.send(f"banned member:\n  '{member}'\nfor reason:\n  '{reason}'")
        return

@ban.error
async def ban_error(message, error):
    if isinstance(error, commands.MissingPermissions):
        await message.send("sorry, you dont have permissions to do that!")
    print(error)

@client.command(description="Unbans the specified user.")
@commands.has_permissions(ban_members=True)
async def unban(message, *, member):
    banned_users = await message.guild.bans()
    print(member)

    for ban_entry in banned_users:
        user = ban_entry.user
        print(user.mention)
        mention = user.mention[0:2] + "!" + user.mention[2:-1] + user.mention[-1]
        print(mention)
        if (mention) == (member):
            await message.guild.unban(user)
            await message.send(f'Unbanned {user.mention}')
            return

@unban.error
async def unban_error(message, error):
    if isinstance(error, commands.MissingPermissions):
        await message.send("sorry, you dont have permissions to do that!")
    print(error)


@client.command(description = "Mutes a specified user.")
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.add_roles(mutedRole)
   await member.send(f"you have been muted on server: {ctx.guild.name}")
   await ctx.send(f"muted: {member.mention}")



@client.command(description = "Unmutes a specified user.")
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.remove_roles(mutedRole)
   await member.send(f"you have been unmuted on server: {ctx.guild.name}")
   await ctx.send(f"unmuted: {member.mention}")




@client.command()
async def rules(message):
    embed = discord.Embed(title="rules:", description = "the rules of the server:", color = discord.Colour.purple())
    embed.add_field(name = "1:", value = "please keep bad language to a minimum", inline = True)
    embed.add_field(name = "2:", value = "no NSFW content of any kind or links to such, this also includes malicious content or links", inline = True)
    embed.add_field(name = "3:", value = "please keep this server friendly and relaxed", inline = True)
    embed.add_field(name = "4:", value = "avoid controversial or political topics", inline = True)
    embed.add_field(name = "5:", value = "absolutely no bullying or discrimination", inline = True)
    embed.add_field(name = "6:", value = "please send messages in the correct channels; keep things relevant", inline = True)
    embed.add_field(name = "7:", value = "please dont ping the owners / admins unless it is important, it gets annoying", inline = True)

    await message.send(embed = embed)


@client.command()
async def rickroll(ctx):
    channel = ctx.message.channel
    await channel.send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")

@client.command()
async def calc(ctx, *, args):
    eq = ""
    equation = ""
    for arg in args:
        eq = f"{eq}{arg}"
    for char in eq:
        if char != " ":
            equation += str(char)
    channel = ctx.message.channel
    await channel.send(f"the answer to {eq} is {calculate(equation)}")

@client.command()
async def docs(message):
    await message.send("you can find my documentation here:")
    embed = discord.Embed(title = "https://fantasypvp.github.io/CrystalDocs")
    await message.send(embed = embed)

@client.command()
async def rickrollvc(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = discord.FFmpegPCMAudio("rickroll.mp3")
        player = voice.play(source)

@client.command()
async def dc(message):
    voice = discord.utils.get(client.voice_clients, guild = message.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await message.send(random.choice["uhm im not in a vc", "im not connected to a voice channel"])



@client.event
async def on_ready():
        await client.change_presence(status = discord.Status.idle, activity = discord.Game("Im back with a better AI than ever thanks to neural networks!"))


@client.event
async def on_message(message):
    if message.author == client.user:
        print(message.content)
        return

    language_used = []
    for word in banned_words.banned_words:
        if word in message.content:
            language_used.append(word)
    if len(language_used) != 0:
        try:
            await logger.filter(message, language_used)
            return
        except:
            pass


    if message.content.startswith(". "):
        response = chatbot.request(message.content[2:])
        print(f"{message.content}\n >> {response}")
        await message.channel.send(response)
        return

    await client.process_commands(message)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi, Im Crystal")

global logger
logger = Logger()

client.run(token)
