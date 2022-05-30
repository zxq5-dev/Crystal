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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(". "):
        response = chatbot.request(message.content[2:])
        await message.channel.send(response)


client.run(token)

