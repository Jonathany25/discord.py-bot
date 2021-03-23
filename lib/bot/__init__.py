from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = ";"
OWNER_IDS = [301305436529754113]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.schedule = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

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

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(803807202032091146)
            self.ready = True

            print("Bot Ready!")

        else:
            print("Bot Reconnected!")

    async def on_message(self, message):
        pass


bot = Bot()
