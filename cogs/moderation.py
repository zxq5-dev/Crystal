import discord
from discord.ext import commands
import random


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, description="Clears the number of messages specified in the channel")
    async def clear(self, message, args):
        amount = args
        messages = []
        async for msg in message.channel.history(limit=int(amount)+1):
            messages.append(msg)
        await message.channel.delete_messages(messages)

    @commands.command()
    async def profile(self, message, member: discord.Member, description="Displays the profile of the specified user."):
        embed = discord.Embed(
            title=member.name, description=member.mention, color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await message.send(embed=embed)

    @commands.command(description="Kicks the specified user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, message, member: discord.Member, *, reason=None):
        if member == commands.user:
            await message.send(embed=discord.Embed(title=random.choice(["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna kick myself!"]), colour=discord.Colour.red()))

        elif member.top_role >= message.author.top_role:
            await message.send(embed=discord.Embed(title=random.choice(["you cant kick members with higher permissions than yours", "sorry, you cant do that", "nice try :)"]), colour=discord.Colour.red()))

        elif member == message.author:
            await message.send(embed=discord.Embed(title=random.choice(["lmao why would you want to kick yourself", "are you sure you want to do that?", "you cant kick yourself lol"]), colour=discord.Colour.red()))

        else:
            await member.kick(reason=reason)
            await member.send(embed=discord.Embed(title=f"you have been kicked from server: {message.guild.name}", color=discord.Colour.red()))
            await message.send(embed=discord.Embed(title=f"kicked member:\n  '{member}'\nfor reason:\n  '{reason}'", color=discord.Colour.green()))

    @kick.error
    async def kick_error(self, message, error):
        if isinstance(error, commands.MissingPermissions):
            await message.send(embed=discord.Embed(title=f"sorry you dont have permission to do that!", color=discord.Colour.red()))

    @commands.command(description="Bans the specified user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, message, member: discord.Member, *, reason=None):
        if member == commands.user:
            await message.send(random.choice(["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna ban myself!"]))
            return
        elif member.top_role >= message.author.top_role:
            await message.send(random.choice(["you cant ban members with higher permissions than yours", "sorry, you cant do that", "nice try :)"]))
            return

        elif member == message.author:
            await message.send(random.choice(["lmao why would you want to ban yourself", "are you sure you want to do that?", "you cant ban yourself lol"]))
            return

        else:
            await member.ban(reason=reason)
            await member.send(embed=discord.Embed(title=f"you have been banned from server: {message.guild.name}", color=discord.Colour.red()))
            await message.send(embed=discord.Embed(title=f"banned member:\n  '{member}'\nfor reason:\n  '{reason}'", color=discord.Colour.green()))
            return

    @ban.error
    async def ban_error(self, message, error):
        if isinstance(error, commands.MissingPermissions):
            await message.send(embed=discord.Embed(title=f"sorry you dont have permission to do that!", color=discord.Colour.red()))

    @commands.command(description="Unbans the specified user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, message, *, member):
        banned_users = await message.guild.bans()
        print(member)

        for ban_entry in banned_users:
            user = ban_entry.user
            print(user.mention)
            mention = user.mention[0:2] + "!" + \
                user.mention[2:-1] + user.mention[-1]
            print(mention)
            if (mention) == (member):
                await message.guild.unban(user)
                await member.send(embed=discord.Embed(title=f"you have been banned from server: {message.guild.name}", color=discord.Colour.red()))
                await message.send(embed=discord.Embed(title=f"banned: {member.mention}", color=discord.Colour.green()))
                return

    @unban.error
    async def unban_error(self, message, error):
        if isinstance(error, commands.MissingPermissions):
            await message.send(embed=discord.Embed(title=f"sorry you dont have permission to do that!", color=discord.Colour.red()))
        print(error)

    @commands.command(description="Mutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, message, member: discord.Member):
        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
        await member.add_roles(mutedRole)
        await member.send(embed=discord.Embed(title=f"you have been muted on server: {message.guild.name}", color=discord.Colour.red()))
        await message.send(embed=discord.Embed(title=f"muted: {member.mention}", color=discord.Colour.green()))

    """
    @mute.error
    async def mute_error(message, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(title = f"sorry you dont have permission to do that!", color = discord.Colour.red()))
        print(error)
    """

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, message, member: discord.Member):
        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await member.send(embed=discord.Embed(title=f"you have been unmuted on server: {message.guild.name}", color=discord.Colour.green()))
        await message.send(embed=discord.Embed(title=f"unmuted: {member.mention}", color=discord.Colour.green()))

    """
    @unmute.error
    async def unmute_error(message, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(title = f"sorry you dont have permission to do that!", color = discord.Colour.red()))
        print(error)
    """

    @commands.command()
    async def rules(self, message):
        embed = discord.Embed(
            title="rules:", description="the rules of the server:", color=discord.Colour.blue())
        embed.add_field(
            name="1:", value="please keep bad language to a minimum", inline=True)
        embed.add_field(
            name="2:", value="no NSFW content of any kind or links to such, this also includes malicious content or links", inline=True)
        embed.add_field(
            name="3:", value="please keep this server friendly and relaxed", inline=True)
        embed.add_field(
            name="4:", value="avoid controversial or political topics", inline=True)
        embed.add_field(
            name="5:", value="absolutely no bullying or discrimination", inline=True)
        embed.add_field(
            name="6:", value="please send messages in the correct channels; keep things relevant", inline=True)
        embed.add_field(
            name="7:", value="please dont ping the owners / admins unless it is important, it gets annoying", inline=True)

        await message.send(embed=embed)


    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def poll(self, message, question, *options: str):

        if len(options) > 2:
            await message.send("invalid syntax, syntax:\n$ poll question, option1, option2")
            return
        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['✅', '❌']
        else:
            reactions = ['✅', '❌']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)

        msg = await message.send(discord.Embed(title=question, color = discord.Colours.blue(), description=''.join(description)))
        for reaction in reactions[:len(options)]:
            await msg.add_reaction(reaction)



def setup(client):
    client.add_cog(Moderation(client))
