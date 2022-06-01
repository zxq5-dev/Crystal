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

client = commands.Bot(command_prefix="$ ")


class Logger():
    async def filter(self, message, words):
        if os.path.exists(f"./data/{message.guild.name}"):
            async with aiofiles.open(f"./data/{message.guild.name}/chat_filter.log", mode="a") as logfile:
                await logfile.write(f"[{get_time()}] : in channel: {message.channel}\n {message.author} used banned words: {words}\nin message: {message.content}\n\n")
        else:
            os.mkdir(f"./data/{message.guild.name}")
            async with aiofiles.open(f"./data/{message.guild.name}/chat_filter.log", mode="a") as logfile:
                await logfile.write(f"[{get_time()}] : in channel: {message.channel}\n {message.author} used banned words: {words}\nin message: {message.content}\n\n")


def get_time():
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    return(time)


@client.command()
async def load(message, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(message, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def rickroll(message):
    await message.send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")


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
    embed = discord.Embed(title="https://fantasypvp.github.io/CrystalDocs")
    await message.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Im back with a better AI than ever thanks to neural networks!"))


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
        if message.channel.type != discord.ChannelType.private:
            await logger.filter(message, language_used)
            await message.channel.send(random.choice(["hey watch your language.", "language!", "could you stop using that kind of language?"]))
            await message.delete()
            return

    if message.content.startswith(". "):
        response = chatbot.request(message.content[2:])
        print(f"{message.author}{message.content}\n >> {response}")
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
logger = Logger()

chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()

client.run(os.environ["token"])
