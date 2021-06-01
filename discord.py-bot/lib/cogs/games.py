from random import choice

from discord import Embed
from discord.ext.commands import Cog, command, BucketType, cooldown


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("games")

    @command(name="gamble", aliases=["choose", "pick"])
    @cooldown(1, 1, BucketType.user)
    async def pick_card(self, ctx, guess, second_guess, bet):

        if bet.isdigit() and guess.isdigit() and second_guess.isdigit():

            if 1 <= int(guess) <= 13 and 1 <= int(second_guess) <= 13:
                bet = int(bet)

                if bet >= 0:
                    guesses = [guess, second_guess]
                    deck = [[number for number in range(1, 14)] for _ in range(4)]
                    rolls = [str(choice(choice(deck))) for _ in range(4)]
                    embed = Embed(title="You got:", description=" ".join(rolls), colour=ctx.author.colour)

                    correct_guess = 0
                    for number in rolls:
                        if number in guesses:
                            correct_guess += 1

                    if correct_guess == 0:
                        embed.add_field(name="You lost:", value=bet)

                    else:
                        final_value = (0.2 + 1 + 0.2 * correct_guess) * bet
                        embed.add_field(name="You got:", value=final_value)

                    await ctx.send(ctx.author.mention, embed=embed)

                else:
                    await ctx.send("You cannot bet less than 0 coins.")

            else:
                await ctx.send("Your guesses have to be between 1 and 13.")

        elif not bet.isdigit() and (not guess.isdigit() or not second_guess.isdigit()):
            await ctx.send("Your bet and both guesses must be valid integer.")

        elif not bet.isdigit():
            await ctx.send("Your bet must be an valid integer.")

        elif not guess.isdigit() or not second_guess.isdigit():
            await ctx.send("Your guesses must be valid integers.")


def setup(bot):
    bot.add_cog(Games(bot))
