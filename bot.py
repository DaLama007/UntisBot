import discord
import dotenv as de
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary = r"C:\Users\Marwan\Desktop\Firefox.exe"
intents = discord.Intents.default()
intents.members = True

de.load_dotenv()
cookies = {'JSESSIONID':os.getenv('UNTIS_TOKEN')}
url_prefix = os.getenv('SCHOOL_PREFIX')

class UntisBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        if(message.content == "!hw"):
            url = url_prefix+ 'WebUntis/api/homeworks/lessons?startDate=20260301&endDate=20260331'
            r = requests.get(url,cookies=cookies)
            try:
                await self.send_homework()
            except Exception as e:
                self.getcookie()
                await self.send_homework()

    async def send_homework(self):
        data = r.json()
        homeworks = data['data']['homeworks']
        for homework in homeworks:
            await channel.send(homework['text'])
    
    def getcookie(self):
        driver = webdriver.Firefox(options=options)
        driver.get(url_prefix+'WebUntis/#/basic/login')
        driver.find_element_by_css_selector('.redesigned-button.mt-1').click()
        time.sleep(3)
        print(driver.page_source)

UB = UntisBot(intents = intents)
UB.run(os.getenv('DISCORD_TOKEN'))
