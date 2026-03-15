import discord
import dotenv as de
import os
import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
import pickle

#set options for selenium browser
options = Options()
options.binary = r"C:\Users\Marwan\Desktop\Firefox.exe"
#options.headless = True

#set intents for discord bot
intents = discord.Intents.default()
intents.message_content = True

#load and save needed variables
de.load_dotenv()
url_prefix = os.getenv('SCHOOL_PREFIX')

class UntisBot(discord.Client):
    cookies = {'JSESSIONID':'helo'}
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        if(message.content == "!hw"):

            #get current date and calculate date in 3 months
            #request url
            url = url_prefix+ 'WebUntis/api/homeworks/lessons?startDate=20260300&endDate=20260331' 
            r = requests.get(url,cookies=self.cookies)

            #try because cookie might be expired
            try:
                await self.send_homework(r,channel)
            except Exception as e:
                #if expired generate new cookie
                capturedCookie = self.getcookie()
                new_cookie = {'JSESSIONID' : capturedCookie['value']}
                self.cookies = new_cookie
                r = requests.get(url,cookies=new_cookie)
                await self.send_homework(r,channel)

    async def send_homework(self,r,channel):
        print(r)
        #parse data
        data = r.json()
        homeworks = data['data']['homeworks']
        
        #get current year in same format
        cdate = datetime.datetime.now()
        formatted_cdate = str(cdate.year) 
        if len(str(cdate.month))==1:
            formatted_cdate+='0'
        formatted_cdate+= str(cdate.month) 
        if len(str(cdate.day))==1:
            formatted_cdate+='0'
        formatted_cdate+= str(cdate.day)
        print(formatted_cdate)

        #loop for every homework
        for homework in homeworks:
            
            #check if homewoirk is yet to come
            if(homework['dueDate']>= int(formatted_cdate)):
                #send homework into same channel
                await channel.send(homework['text'] + " "+ str(homework['dueDate']))
            
    
    def getcookie(self):
        driver = webdriver.Firefox(options=options)
        driver.get(url_prefix+'WebUntis/#/basic/login')
        
        #get credentials from env
        UN = os.getenv('UNTIS_UN')
        PW = os.getenv('UNTIS_PASS')
        
        #click login button
        driver.find_element(By.CSS_SELECTOR, ".redesigned-button.mt-1").click()
        time.sleep(1)

        #fill input box for username and click button element for first login
        username = driver.find_element(By.ID, "username")
        username.send_keys(UN)
        driver.find_element(By.CSS_SELECTOR, ".pure-button.pure-button-red").click()
        time.sleep(1)
        
        #get input box password
        password = driver.find_element(By.ID, "password")
        
        #input
        password.send_keys(PW)
        
        #submit and wait
        driver.find_element(By.CSS_SELECTOR, ".pure-button.pure-button-red").click()
        time.sleep(4)

        #return the cookie of that page
        driver.get(url_prefix+'WebUntis')
        cookie = driver.get_cookie('JSESSIONID')
        print(cookie)
        time.sleep(5)
        driver.quit()
        return cookie

UB = UntisBot(intents = intents)
UB.run(os.getenv('DISCORD_TOKEN'))
