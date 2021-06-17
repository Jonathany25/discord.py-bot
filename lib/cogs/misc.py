import json
from typing import Optional

import discord
from discord import Embed
from discord.ext.commands import CheckFailure, has_role, check_any, is_owner
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.menus import ListPageSource

from ..db import db


# class ChannelMenu(ListPageSource):
# def __init__(self, ctx, data):
# self.ctx = ctx

# super().__init__(data, per_page=9)


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if ctx.channel.id == self.bot.channels["Configs"]:
            if len(new) > 5:
                await ctx.send("The prefix can not be more than 5 characters in length.")

            else:
                with open("./lib/bot/configs.json", "r+") as f:
                    data = json.load(f)
                    data["PREFIX"] = new
                with open("./lib/bot/configs.json", "w") as f:
                    json.dump(data, f)

                await ctx.send(f"Prefix set to '{new}'.")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @command(name="register")
    @check_any(is_owner())
    async def register(self, ctx):
        if ctx.channel.id == self.bot.channels["Configs"]:
            registered_members = db.records("SELECT UserID FROM bal")
            registered_members = [member[0] for member in registered_members]

            members = [member for member in self.bot.guild.members if
                       (not member.bot) and (member.id not in registered_members)]
            await ctx.send(f"Started registering {len(members)} members.")

            for member in members:
                db.execute("INSERT INTO bal (UserID) VALUES (?);", member.id)

            await ctx.send(f"Finished registering {len(members)} members.")

    @register.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need to be a bot owner. to do that.")

    @command(name="channel", aliases=["channels"])
    @has_permissions(manage_guild=True)
    async def set_channel(self, ctx, category: Optional[str], channel: Optional[discord.TextChannel]):
        if category is None:
            embed = Embed(title="Channels", colour=ctx.author.color)
            for channel in self.bot.channels:
                embed.add_field(name=channel, value=self.bot.get_channel(self.bot.channels[channel]).mention)
            await ctx.send(embed=embed)

        else:
            if category not in self.bot.channels:
                await ctx.send("Please input a valid category.")

            elif channel is None:
                await ctx.send("Please input a valid channel.")

            else:
                self.bot.channels[category] = channel.id

                with open("./lib/bot/configs.json", "r+") as f:
                    data = json.load(f)
                    data["channels"] = self.bot.channels
                with open("./lib/bot/configs.json", "w") as f:
                    json.dump(data, f)

                await ctx.send(f"Changed {category} channel to {channel.mention}.")

    @set_channel.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


def setup(bot):
    bot.add_cog(Misc(bot))
