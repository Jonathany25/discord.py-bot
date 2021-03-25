from random import randint

from discord import Embed
from discord.ext.commands import Cog, command


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

    @command(name="dice_roll", aliases=["dice", "roll"])
    async def dice_roll(self, ctx, roll="1"):
        if (not roll.isdigit()) or int(roll) == 0:
            await ctx.send("The number of rolls must be a non-zero integer.")
        elif int(roll) > 10:
            await ctx.send("Cannot roll more than 10 die at a time.")
        else:
            rolls = [str(randint(1, 10)) for _ in range(int(roll))]
            embed = Embed(title="You rolled:", description=" ".join(rolls))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
