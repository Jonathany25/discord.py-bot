from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext.commands import Bot as BotBase, CommandNotFound

from ..db import db

PREFIX = ";"
OWNER_IDS = [301305436529754113]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as token_file:
            self.TOKEN = token_file.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot Disconnected!")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong!")  # args[0] is an object we can send a message back to

            raise

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):  # checks if exception is CommandNotFound error
            pass

        elif hasattr(exception, "original"):
            raise exception.original  # raises original exception, it is simpler to read

        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(803807202032091146)
            self.scheduler.start()
            self.ready = True

            print("Bot Ready!")

        else:
            print("Bot Reconnected!")

    async def on_message(self, message):
        pass


bot = Bot()
