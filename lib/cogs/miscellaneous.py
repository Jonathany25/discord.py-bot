from aiohttp import request
from discord import Embed, Member
from discord.ext.commands import Cog, command, BadArgument, BucketType, cooldown


class Miscellaneous(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("miscellaneous")

    @command(name="quote", aliases=["inspire"])
    @cooldown(1, 2, BucketType.user)
    async def send_random_quote(self, ctx):
        URL = "https://zenquotes.io/api/random"
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json(content_type="text/plain")
                quote = f"{data[0]['q']}\n-{data[0]['a']}-"
                await ctx.send(quote)
            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(name="meme", aliases=[])
    @cooldown(1, 2, BucketType.user)
    async def send_meme(self, ctx):
        URL = "https://meme-api.herokuapp.com/gimme"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(colour=0x42b9f5, url=data['postLink'])
                embed.title = f"r/{data['subreddit']}\n{data['title']}"
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(name="slap", aliases=["hit"])
    @cooldown(1, 1, BucketType.user)
    async def slap_member(self, ctx, member: Member, *, reason="no reason."):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I cannot find that member.")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
