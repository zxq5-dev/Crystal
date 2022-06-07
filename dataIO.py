import json
import os
import aiofiles
from datetime import datetime
import discord


def get_time():
    now = datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    return(time)


def get_int(time):
    integer = ""
    for char in time:
        if char.isnumeric():
            integer += char
    integer = int(integer)
    return(integer)


def validate_time(time):
    while time[5] >= 60:
        time[5] -= 60
        time[4] += 1
    while time[4] >= 60:
        time[4] -= 60
        time[3] += 1
    while time[3] >= 24:
        time[3] -= 12
        time[2] += 1
    while time[2] >= 30:
        time[2] -= 30
        time[1] += 1
    while time[1] >= 12:
        time[1] -= 12
        time[0] += 1
    t2 = []
    for t in time:
        if len(str(t)) == 1:
            t2.append(f"0{str(t)}")
        else:
            t2.append(str(t))
    return(f"{t2[0]}-{t2[1]}-{t2[2]}-{t2[3]}-{t2[4]}-{t2[5]}")


def convert_time(time):
    duration = [0, 0, 0, 0, 0, 0]
    if time.endswith("s"):
        duration[5] = int(time[:-1])
    if time.endswith("m"):
        duration[4] = int(time[:-1])
    if time.endswith("h"):
        duration[3] = int(time[:-1])
    if time.endswith("d"):
        duration[2] = int(time[:-1])
    if time.endswith("y"):
        duration[0] = int(time[:-1])
    duration = validate_time(duration)

    return(duration)


def get_date(duration):
    time = get_time()
    newtime = []
    newduration = []

    for x in time.split("-"):
        newtime.append(int(x))

    for x in duration.split("-"):
        newduration.append(int(x))

    finaltime = []
    for x in range(6):
        finaltime.append(newtime[x] + newduration[x])

    finaltime = validate_time(finaltime)
    return(finaltime)


class Logger():
    async def filter(self, message, words):
        if not os.path.exists(f"./data/{message.guild.id}"):
            os.mkdir(f"./data/{message.guild.id}")

        async with aiofiles.open(f"./data/{message.guild.id}/chat_filter.log", mode="a") as logfile:
            await logfile.write(f"[{get_time()}] | channel: {message.channel} | user: {message.author} [{message.author.mention}] | used banned words: {words} \nin message: {message.content}\n\n")
            return


class Guild_data():
    def __init__(self, guild, setup):
        if not os.path.exists(f"./data/{guild.id}"):
            os.mkdir(f"./data/{guild.id}")

        if not os.path.exists(f"./data/{guild.id}/chat_filter.log"):
            file = open(f"./data/{guild.id}/chat_filter.log", "w")
            file.write(
                f"\n# chat filter logs from server {guild.name} [{guild.id}]\n\n"
            )

        if not os.path.exists(f"./data/{guild.id}/server_data.json"):
            file = open(f"./data/{guild.id}/server_data.json", "w")
            file.write('{ "test" : "test" }')
            file.close()
            if setup == False:
                return("You have not setup my functions on this server yet! to do so run '$ setup' this is necessary in order to store any data about the guild")

        self.filename = f"./data/{guild.id}/server_data.json"
        with open(self.filename) as file:
            self.data = json.load(file)
        return

    def update(self):
        with open(self.filename, "w") as file:
            data = json.dumps(self.data, sort_keys=True, indent=4)
            file.write(data)

    def get_user(self, member):

        self.data["members"][member.mention]["mention"] = member.mention
        self.data["members"][member.mention]["id"] = member.id
        self.data["members"][member.mention]["known-name"] = member.name
        data = self.data["members"][member.mention]
        return(data)
        self.update()

    def get_rules(self):
        rules = []
        for rule in self.data["server-rules"]:
            rules.append((rule, self.data["server-rules"][rule]))
        return(rules)  # returns a tuple (name, description)

    def add_rule(self, rule):
        # rule is a tuple (name, description)
        self.data["server-rules"][rule[0]] = f"{rule[1]}"
        print(dict(sorted(self.data["server-rules"].items())))
        self.data["server-rules"] = dict(
            sorted(self.data["server-rules"].items())
        )

        self.update()
        return("Successfully added rule")

    def remove_rule(self, rule):
        if rule in self.data["server-rules"]:
            del self.data["server-rules"][rule]
            self.update()
            return("Successfully removed rule")
        else:
            self.update()
            return("This rule does not exist, try providing the number / name of the role and not the description")

    def get_bans(self):
        bans = []
        if "ban-list" in self.data:
            for ban in self.data["ban-list"]:
                bans.append(ban)
        else:
            bans.append(None)
        self.update()
        return

    def get_mutes(self):
        bans = []
        if "mute-list" in self.data:
            for ban in self.data["mute-list"]:
                mutes.append(mute)
        else:
            mutes.append(None)
        self.update()
        return

    def update_bans(self, guild, ban_profile):
        if ban_profile != None:
            self.data["ban-list"][ban_profile.user_id] = {
                "reason": f"{ban_profile.reason}",
                "initial-duration": f"{ban_profile.duration}",
                "expiry-date": f"{ban_profile.expiry}"
            }
        # updates all bans
        removes = []
        for ban in self.data["ban-list"]:
            if get_int(self.data["ban-list"][ban]["expiry-date"]) <= get_int(get_time()):
                removes.append(ban)
        for ban in removes:
            del self.data["ban-list"][ban]
        self.update()
        return

    def update_mutes(self, guild, mute_profile):
        if mute_profile != None:
            self.data["mute-list"][mute_profile.user_id] = {
                "reason": f"{mute_profile.reason}",
                "initial-duration": f"{mute_profile.duration}",
                "expiry-date": f"{mute_profile.expiry}"
            }
        # updates all mutes
        removes = []
        print(self.data["mute-list"])
        for mute in self.data["mute-list"]:
            print(get_int(self.data["mute-list"][mute]
                          ["expiry-date"]), get_int(get_time()))
            if get_int(self.data["mute-list"][mute]["expiry-date"]) <= get_int(get_time()):
                removes.append(mute)
        for mute in removes:
            del self.data["mute-list"][mute]
        self.update()
        return

    def add_suggestion(self, member, suggestion):
        self.data["suggestions"][get_time()] = {
            "mention": f"{member.mention}",
            "suggestion": f"{suggestion}"
        }
        self.update()
        return

    async def server_setup(self, guild, channels):

        default_rules = {
            "1:": "please keep bad language to a minimum",
            "2:": "no NSFW content of any kind or links to such, this also includes malicious content or links",
            "3:": "please keep this server friendly and relaxed",
            "4:": "avoid controversial or political topics",
            "5:": "absolutely no bullying or discrimination",
            "6:": "please send messages in the correct channels; keep things relevant",
            "7:": "please dont ping the owners / admins unless it is important, it gets annoying"
        }

        self.data = {
            "header": {
                "server-name": f"{guild.name}",
                "server-id": f"{guild.id}",
                "server-owner": f"{guild.owner_id}"
            },
            "members": {},
            "ban-list": {},
            "mute-list": {},
            "channels": channels,
            "server-prefixes": {"moderation": "$ ", "chatbot": ". ", "normal": "? "},
            "server-suggestions": {},
            "server-rules": default_rules
        }
        for member in guild.members:
            try:
                await guild.fetch_ban(member)
                expiry = "never"
            except discord.NotFound:
                expiry = "none"

            self.data["members"][f"{member.mention}"] = {
                "known-name": f"{member.name}",
                "mention": f"{member.mention}",
                "id": f"{member.id}",
                "punishments": {
                    "ban-reason": "none",
                    "ban-expiry": f"{expiry}",
                    "mute-reason": "none",
                    "mute-expiry": "none"
                },
                "level": "1"
            }
        self.update()

        return


class Punishment_profile():
    def __init__(self, user_id, duration, expiry, reason):
        self.user_id = user_id
        self.duration = duration
        self.expiry = expiry
        self.reason = reason
