from random import choice

from discord import Embed
from discord.ext.commands import Cog, command


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("games")

    @command(name="pick_card", aliases=["gamble"])
    async def pick_card(self, ctx, guess, bet="0"):
        if bet.isdigit() and guess.isdigit():
            bet = int(bet)
            if bet >= 0:
                deck = [[number for number in range(1, 14)] for _ in range(4)]
                rolls = [str(choice(choice(deck))) for _ in range(4)]
                embed = Embed(title="You got:", description=" ".join(rolls))

                correct_guess = 0
                for number in rolls:
                    if number == guess:
                        correct_guess += 1

                if correct_guess == 0:
                    embed.add_field(name="You lost:", value=bet)
                else:
                    final_value = (0.2 + 1 + 0.2 * correct_guess) * bet
                    embed.add_field(name="You got:", value=final_value)

                await ctx.send(embed=embed)

            else:
                await ctx.send("You cannot bet less than 0 coins.")

        elif not bet.isdigit() and not guess.isdigit():
            await ctx.send("Your bet and guess must be valid integer.")

        elif not bet.isdigit():
            await ctx.send("Your bet must be an valid integer.")

        elif not guess.isdigit():
            await ctx.send("Your guess must be a valid integer.")


def setup(bot):
    bot.add_cog(Games(bot))
