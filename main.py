import discord
from neuralintents import GenericAssistant
from dotenv import load_dotenv
import os



chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()


client = discord.Client()

load_dotenv()
token = os.getenv("token")

def calc(equation):
    return 1

async def exec_command(message):
    command = message.content[2:]
    if len(command) < 4:
        await message.channel.send("hmm that command doesnt make sense, try '$ help'")
        return
    cmd_base = command[:4]

    if cmd_base == "calc":
        await message.channel.send(f"the answer to {command[5:]} is: {calc(command[5:])}")
        return
    if cmd_base == "help":
        await message.channel.send(f"""
you can chat to me by prefixing messages with '. '
you can also run commands by typing '$ (command) [args]', for example:
    '$ calc 1+1'
    '$ roll user*'
""")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(". "):
        response = chatbot.request(message.content[2:])
        await message.channel.send(response)
        return

    if message.content.startswith("$ "):
        await exec_command(message)
        return
    return

client.run(token)
