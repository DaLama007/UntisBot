import discord
import dotenv as de
import os

de.load_dotenv()

class UntisBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
       print(f'Message from {message.author}: {message.author}')

UB = UntisBot()
UB.run(os.getenv('DISCORD_TOKEN'))
