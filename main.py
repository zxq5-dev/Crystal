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
import dataIO

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix="$ ", intents=intents)


def get_time():
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    return(time)


@client.command()
async def setup(message):

    overwrites = {message.guild.default_role: discord.PermissionOverwrite(
        read_messages=False), }
    sys_channel = await message.guild.create_text_channel('Crystal-System-Channel', overwrites=overwrites)
    await sys_channel.send(f"<@{message.guild.owner.id}>")

    overwrites = {message.guild.default_role: discord.PermissionOverwrite(
        read_messages=False), }
    changelogs_channel = await message.guild.create_text_channel('Crystal-Changelogs', overwrites=overwrites)
    await changelogs_channel.send(f"<@{message.guild.owner.id}> This is where logs of major changes to my code will appear!")

    overwrites = {message.guild.default_role: discord.PermissionOverwrite(
        send_messages=False), }
    rules_channel = await message.guild.create_text_channel('Rules', overwrites=overwrites)
    await rules_channel.send(f"<@{message.guild.owner.id}>")

    overwrites = {message.guild.default_role: discord.PermissionOverwrite(
        read_messages=False), }
    logs_channel = await message.guild.create_text_channel('logs', overwrites=overwrites)
    await logs_channel.send(f"<@{message.guild.owner.id}> This is where all of your logs will appear, these include ")

    channels = {
        "rules-channel": rules_channel.id,
        "sys-channel": sys_channel.id,
        "changelogs-channel": changelogs_channel.id,
        "logs-channel": logs_channel.id
    }

    server_data = dataIO.Guild_data(message.guild, True)
    await server_data.server_setup(message.guild, channels)

    # posting first embed
    embed = discord.Embed(title="Crystal-System-Channel",
                          colour=discord.Colour.blue())
    embed.add_field(name="this channel", value="I have created this channel as a system channel where you can request from me potentially sensitive information about the server.", inline=False)
    embed.add_field(name="purpose", value="you will be able to request the logs and data of your server using a custom command (use '$ help' for info) however you will not be able to send that data back to me. any changes you want to make must be made through my commands", inline=False)
    embed.add_field(name="warning:", value="ensure that you do not run the setup command again or else you risk losing all of the data that i have recorded including logs, temporary bans, and config", inline=False)
    embed.add_field(name="one more thing", value="I strongly recommend that you run '$ help' and '$ docs' before you do anything else, In fact I recommend it so strongly that i will leave the link below along with any other information you will need!", inline=False)
    await sys_channel.send(embed=embed)

    # posting link to documentation
    embed = discord.Embed(
        title="https://fantasypvp.github.io/CrystalDocs", colour=discord.Colour.blue())
    await sys_channel.send(embed=embed)

    # setting up rules
    embed = discord.Embed(
        title="rules:", description="the rules of the server:", color=discord.Colour.blue())
    for rule in server_data.get_rules():
        embed.add_field(name=f"{rule[0]}", value=f"{rule[1]}", inline=False)
    embed.set_footer(
        text="you can add or remove rules at any time with '$ rules add rulename rule-description' and '$ rules remove rulename'")
    await rules_channel.send(embed=embed)


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
async def load(message, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(message, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def rickroll(message, *args):
    if len(args) == 1:
        if args[0] == "remove":
            async for msg in message.channel.history(limit=30):
                if "$ rickroll" in msg.content:
                    await msg.delete()
                elif "https://tenor.com" in msg.content and ("rickroll" in msg.content or "rick-roll" in msg.content):
                    await msg.delete()
            return
    async for msg in message.channel.history(limit=10):
        if "@everyone" in msg.content:
            await message.send("nice try bozo")
            return
    await message.send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")


@client.command()
async def docs(message):
    await message.send("you can find my documentation here:")
    embed = discord.Embed(title="https://fantasypvp.github.io/CrystalDocs")
    await message.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("$ rules, you know them and so do I!"))


@client.event
async def on_message(message):
    print(message.content)
    if "@everyone" in message.content:
        rolls = 0
        async for msg in message.channel.history(limit=20):
            if "https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713" in msg.content:
                await msg.delete()
                rolls = 1
        if rolls == 1:
            await message.send("all recent rickrolls have been removed because you pinged everyone")

    if message.author == client.user:

        return

    language_used = []
    for word in banned_words.banned_words:
        if word in message.content.lower():
            language_used.append(word)
    if len(language_used) != 0:
        if message.channel.type != discord.ChannelType.private:
            await logger.filter(message, language_used)
            await message.channel.send(random.choice(["hey watch your language.", "language!", "could you stop using that kind of language?"]))
            await message.delete()
            return

    if message.content.startswith(". "):
        response = chatbot.request(message.content[2:])
        print(f" >> {response}")
        await message.channel.send(response)
        return

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi, Im Crystal")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


global logger
load_dotenv()
logger = dataIO.Logger()

chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()


client.run(os.environ["token"])
