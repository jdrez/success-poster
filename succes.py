import discord
import asyncio
import requests
import json
import tweepy
import re
import os
import urllib.request
from discord import utils
client = discord.Client()
with open('config.json') as w:
    w = json.load(w)
    CONSUMER_KEY = w["consumer_key"]
    CONSUMER_SECRET = w["consumer_secret"]
    ACCESS_KEY = w["consumer_secret"]
    ACCESS_SECRET = w["access_secret"]
    Btoken = w["Btoken"]
    webhookColor = w["webhookColor"]
    accountName = w["AccountName"]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

global api
api = tweepy.API(auth)
@client.event
async def on_message(message):
    global api
    if message.content.startswith('-ping'):
        await client.send_message(message.channel, 'Success Bot on')
    if str(message.channel.name) == "success":
        try:
            author = str(message.author)
            author = re.split(r'\b#\b', author, maxsplit=1)[0].strip()
            image_url = message.attachments[0]['url']
            tweet_text = ('Success by '+author)
            tweet_image = image_url
            filename = 'temp.jpg'
            request = requests.get(tweet_image, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                upload_tweet = api.update_with_media(filename, status=tweet_text)
                tweet_id = str(upload_tweet.id)
                embed=discord.Embed(title="Tweet Posted!", colour=discord.Colour(webhookColor))
                embed.add_field(name = 'See your tweet here 😃 ', value = 'https://twitter.com/'+str(accountName)+'/status/' + str(tweet_id))
                embed.set_footer(text="{} Success".format(accountName))
                print(str(message.author) + 'just posted success!' +  str(tweet_id))
                sent_msg =  client.send_message(message.channel, embed=embed)
                await client.send_message(message.channel, embed=embed) 
        except IndexError:
           pass

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print("Running on: ")
	for botservers in client.servers: print(str(botservers))
	print('------')
client.run(Btoken)
