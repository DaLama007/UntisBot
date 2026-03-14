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

#set options for selenium browser
options = Options()
options.binary = r"C:\Users\Marwan\Desktop\Firefox.exe"
options.headless = True

#set intents for discord bot
intents = discord.Intents.default()
intents.message_content = True

#load and save needed variables
de.load_dotenv()
cookies = {'JSESSIONID':os.getenv('UNTIS_TOKEN')}
url_prefix = os.getenv('SCHOOL_PREFIX')

class UntisBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        if(message.content == "!hw"):
            #request url
            url = url_prefix+ 'WebUntis/api/homeworks/lessons?startDate=20260301&endDate=20260331' 
            r = requests.get(url,cookies=cookies)

            #try because cookie might be expired
            try:
                await self.send_homework(r,channel)
            except Exception as e:
                #if expired generate new cookie
                self.getcookie()
                await self.send_homework(r,channel)

    async def send_homework(self,r,channel):
        #parse data
        data = r.json()
        homeworks = data['data']['homeworks']

        #loop for every homework
        for homework in homeworks:
            #send homework into same channel
            await channel.send(homework['text'])
    
    def getcookie(self):
        driver = webdriver.Firefox(options=options)
        driver.get(url_prefix+'WebUntis/#/basic/login')
        #click login button
        driver.find_element(By.CSS_SELECTOR, ".redesigned-button.mt-1").click()
        time.sleep(3)

        #get input boxes for username and password
        username = driver.find_element(By.CSS_SELECTOR, ".redesigned-button.mt-1").click()
        password = driver.find_element(By.CSS_SELECTOR, ".redesigned-button.mt-1").click()
        
        #get credentials from env
        creds = {process.getenv(UNTIS_UN),process.getenv(UNTIS_PASS)}
        
        #input
        username.send_keys(creds[0])
        password.send_keys(creds[1])

        time.sleep(3)
        print(driver.page_source)

UB = UntisBot(intents = intents)
UB.run(os.getenv('DISCORD_TOKEN'))
