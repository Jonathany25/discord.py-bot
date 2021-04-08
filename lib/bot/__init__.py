from asyncio import sleep
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase, CommandNotFound, Context, BadArgument, MissingRequiredArgument, \
    CommandOnCooldown

from ..db import db

PREFIX = ";"
OWNER_IDS = [301305436529754113, 333535679130763264, 401962070675030017]
IGNORE_EXCEPTION = (CommandNotFound, BadArgument)
COGS = [path.split("\\")[-1][:-3] for path in
        glob("./lib/cogs/*.py")]  # gets all file names that meet the criteria *.py in the specified path


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} Cog Ready!\n")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")  # used to load a cog
            print(f"{cog} cog loaded.")
        print("\nSetup Complete!")

    def run(self, version):
        self.VERSION = version

        print("Running Setup...\n")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as token_file:
            self.TOKEN = token_file.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:  # checks if a command is sent before the bot is ready
                await self.invoke(ctx)
            else:
                await ctx.send("I am not ready to receive commands, please try again in a few seconds.")

    async def on_connect(self):
        print("Bot Connected!\n")

    async def on_disconnect(self):
        print("Bot Disconnected!\n")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong!")  # args[0] is an object we can send a message back to

            raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in
                IGNORE_EXCEPTION]):  # checks if exception is in the ignore list
            pass

        elif hasattr(exc, "original"):
            raise exc.original  # raises original exception, it is simpler to read

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {exc.retry_after:,.2f} seconds.")

        elif isinstance(exc.original, HTTPException):
            await ctx.send("Unable to send message.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send("I do not have the permission to do that.")

        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True

            print("Bot Ready!\n")

        else:
            print("\nBot Reconnected!\n")

    async def on_message(self, message):
        if self.guild is None:
            self.guild = self.get_guild(message.guild.id)

        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
