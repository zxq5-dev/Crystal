import discord
from discord.ext import commands
import youtube_dl
import asyncio


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rickrollvc(self, message):
        if message.author.voice:
            channel = message.author.voice.channel
            voice = await channel.connect()
            source = discord.FFmpegPCMAudio("rickroll.mp3")
            voice.play(source)

    @commands.command()
    async def play(self, message, url: str):
        try:
            voice_client = await message.author.voice.channel.connect()
        except:
            pass
        try:
            videoID = url.split("watch?v=")[1].split("&")[0]
            voice_clients[voice_client.guild.id] = voice_client
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data["url"]
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice_clients[message.guild.id].play(player)

            embed = discord.Embed(
                title=f"Now playing:", color=discord.Colour.green())
            embed.add_field(name="url:", value=f"[{url}]", inline=False)
            embed.set_image(url=f"https://img.youtube.com/vi/{videoID}/0.jpg")
            await message.send(embed=embed)
        except Exception as err:
            print(err)

    @commands.command()
    async def pause(self, message):
        if not voice_clients[message.guild.id].is_paused():
            voice_clients[message.guild.id].pause()
            embed = discord.Embed(title="Paused Music",
                                  color=discord.Colour.red())
            await message.send(embed=embed)
        else:
            embed = discord.Embed(
                title="I am not already paused!", color=discord.Colour.green())

    @commands.command()
    async def resume(self, message):
        if voice_clients[message.guild.id].is_paused():
            voice_clients[message.guild.id].resume()
            embed = discord.Embed(title="Resumed Music")
            await message.send(embed=embed)
        else:
            embed = discord.Embed(
                title="I am not currently paused!", color=discord.Colour.red())

    @commands.command()
    async def stop(self, message):
        voice_clients[message.guild.id].stop()
        await voice_clients[message.guild.id].disconnect()
        embed = discord.Embed(title="Stopped Music",
                              color=discord.Colour.green())
        await message.send(embed=embed)


def setup(client):
    global voice_clients
    global yt_dl_opts
    global ytdl
    global ffmpeg_options
    voice_clients = {}
    yt_dl_opts = {"format": "bestaudio/best"}
    ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
    ffmpeg_options = {"options": "-vn"}

    client.add_cog(Music(client))
