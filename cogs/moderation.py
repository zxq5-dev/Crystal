import discord
from discord.ext import commands
import random
import dataIO


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
        if member == self.client.user:
            await message.send(embed=discord.Embed(title=random.choice(["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna kick myself!"]), colour=discord.Colour.red()))

        elif member.top_role >= message.author.top_role:
            await message.send(embed=discord.Embed(title=random.choice(["you cant kick members with higher permissions than yours", "sorry, you cant do that", "nice try :)"]), colour=discord.Colour.red()))

        elif member == message.author:
            await message.send(embed=discord.Embed(title=random.choice(["lmao why would you want to kick yourself", "are you sure you want to do that?", "you cant kick yourself lol"]), colour=discord.Colour.red()))

        else:
            await member.kick(reason=reason)
            await member.send(embed=discord.Embed(title=f"you have been kicked from server: {message.guild.name}", color=discord.Colour.red()))
            await message.send(embed=discord.Embed(title=f"kicked member:\n  '{member}'\nfor reason:\n  '{reason}'", color=discord.Colour.green()))

    @commands.command(description="Bans the specified user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, message, member: discord.Member, duration, reason):
        if member == self.client.user:
            await message.send(random.choice(["why are you trying to get rid of me huh? :(", "why would you want to do that :broken_heart:", "why would you do that to me?", "im not gonna ban myself!"]))
            return
        elif member.top_role >= message.author.top_role:
            await message.send(random.choice(["you cant ban members with higher permissions than yours", "sorry, you cant do that", "nice try :)"]))
            return

        elif member == message.author:
            await message.send(random.choice(["lmao why would you want to ban yourself", "are you sure you want to do that?", "you cant ban yourself lol"]))
            return

        else:
            guild_data = dataIO.Guild_data(message.guild, False)
            expiry = dataIO.get_date(dataIO.convert_time(duration))
            guild_data.update_bans(message.guild, dataIO.Punishment_profile(
                member.id, dataIO.convert_time(duration), expiry, reason))
            try:
                await member.send(embed=discord.Embed(title=f"you have been banned from server: {message.guild.name}", color=discord.Colour.red()))
                content = "(successfully notified user)"
            except:
                content = "(failed to notify user)"
            await member.ban(reason=reason)
            await message.send(embed=discord.Embed(title=f"banned member:\n  '{member}'\nfor reason:\n  '{reason}' {content}", color=discord.Colour.green()))
            return

    @commands.command(description="Unbans the specified user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, message, member_mention, reason):
        member = self.client.get_user(member_mention[1:-2])
        guild_data = dataIO.Guild_data(message.guild, False)
        expiry = dataIO.get_time()
        guild_data.update_mutes(message.guild, dataIO.Punishment_profile(
            member.id, "none", expiry, "none"))
        try:
            await member.fetch_ban()
        except:
            await message.send(embed=discord.Embed(title=f"failed to unban user: {message.guild.name}, member is not banned", color=discord.Colour.red()))
            return

        await message.guild.unban(user)
        await member.send(embed=discord.Embed(title=f"you have been banned from server: {message.guild.name}", color=discord.Colour.red()))
        await message.send(embed=discord.Embed(title=f"banned: {member.mention}", color=discord.Colour.green()))
        return

    @commands.command(description="Mutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, message, member: discord.Member, duration, reason):
        guild_data = dataIO.Guild_data(message.guild, False)
        expiry = dataIO.get_date(dataIO.convert_time(duration))
        guild_data.update_mutes(message.guild, dataIO.Punishment_profile(
            member.id, dataIO.convert_time(duration), expiry, reason))
        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
        if mutedRole == None:
            print("huh")
            perms = discord.Permissions(send_messages=False)
            await message.guild.create_role(name="Muted", permissions=perms)
            mutedRole = discord.utils.get(message.guild.roles, name="Muted")
        await member.add_roles(mutedRole)
        await member.send(embed=discord.Embed(title=f"you have been muted on server: {message.guild.name}", color=discord.Colour.red()))
        await message.send(embed=discord.Embed(title=f"muted: {member.name}", color=discord.Colour.green()))

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, message, member: discord.Member):
        guild_data = dataIO.Guild_data(message.guild, False)
        expiry = dataIO.get_time()
        guild_data.update_mutes(message.guild, dataIO.Punishment_profile(
            member.id, "none", expiry, "none"))
        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await member.send(embed=discord.Embed(title=f"you have been unmuted on server: {message.guild.name}", color=discord.Colour.green()))
        await message.send(embed=discord.Embed(title=f"unmuted: {member.name}", color=discord.Colour.green()))

    @commands.command(pass_context=True)
    async def poll(self, message, question, opt1, opt2):

        print(opt1, opt2)
        options = [opt1, opt2]

        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['✅', '❎']
        else:
            reactions = ['✅', '❎']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)

        embed = discord.Embed(title=question, color=3553599,
                              description=''.join(description))

        react_message = await message.send(embed=embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        await react_message.edit_message(embed=embed)

    @commands.command()
    async def rules(self, message, *args):
        guild_data = dataIO.Guild_data(message.guild, False)
        if len(args) != 0:
            if args[0] == "add":
                if len(args) != 3:
                    await message.send("you did not provide the correct number of arguments, try structuring the command like this: '$ rules add \"name of rule\" \"description of rule\"'")
                    return

                name = args[1]
                description = args[2]
                await message.send(guild_data.add_rule((name, description)))
                channel = self.client.get_channel(
                    guild_data.data["channels"]["rules-channel"])

                async for msg in channel.history():
                    await msg.delete()

                embed = discord.Embed(
                    title="Server Rules:", colour=discord.Colour.blue())

                for rule in guild_data.get_rules():
                    embed.add_field(name=rule[0], value=rule[1], inline=False)

                await channel.send(embed=embed)
                return

            elif args[0] == "remove":
                if len(args) != 2:
                    await message.send("you did not provide the correct number of arguments, try structuring the command like this: '$ rules remove \"name of rule\"' you can find out the name of the rule using simply '$ rules'")
                    return

                name = args[1]
                await message.send(guild_data.remove_rule(name))
                channel = self.client.get_channel(
                    guild_data.data["channels"]["rules-channel"])

                async for msg in channel.history():
                    await msg.delete()

                embed = discord.Embed(
                    title="Server Rules:", colour=discord.Colour.blue())

                for rule in guild_data.get_rules():
                    embed.add_field(name=rule[0], value=rule[1], inline=False)

                await channel.send(embed=embed)
                return
            else:
                await message.send("invalid argument, executing as if no args provided.")
        embed = discord.Embed(title="Server Rules:",
                              colour=discord.Colour.blue())
        for rule in guild_data.get_rules():
            embed.add_field(name=rule[0], value=rule[1], inline=False)
        await message.send(embed=embed)
        return


def setup(client):
    client.add_cog(Moderation(client))
