import discord
import dotenv as de
import os
import requests
import json

de.load_dotenv()
cookies = {'JSESSIONID':os.getenv('UNTIS_TOKEN')}
class UntisBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        if(message.content == "!hw"):
            url = os.getenv('SCHOOL_PREFIX') + 'WebUntis/api/homeworks/lessons?startDate=20260301&endDate=20260331'
            r = requests.get(url,cookies=cookies)
            data = r.json()
            homeworks = data['data']['homeworks']
            for homework in homeworks:
                await channel.send(homework['text'])

UB = UntisBot()
UB.run(os.getenv('DISCORD_TOKEN'))
