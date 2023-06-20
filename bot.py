import os 
import requests 
from discord.ext import commands, tasks
import discord 
import json, random, asyncio
from dotenv import load_dotenv


from time import sleep 
from datetime import datetime
import threading

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
GUILD_ID = int(os.getenv('GUILD_TOKEN'))
CHANNEL_ID = int(os.getenv('CHANNEL_TOKEN'))

print(type(CHANNEL_ID))

intents=discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)




@tasks.loop(hours=24)
async def test():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(refresh_data())



#On ready event, displays server members, ID, and server connection 
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    # guild = discord.utils.find(lambda g: g.name == SERVER, client.guilds)
    
    guild = discord.utils.get(client.guilds, name=SERVER)
    
    test.start()

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}')
    
#On member event, welcomes anyone who joins the server
@client.event 
async def on_member_join(member):
    guild = client.get_guild(1103430473633513658)
    channel = guild.get_channel(1103430474338152545)
    await channel.send(f'Welcome to the server {member.mention}!  ')
    await member.create_dm()
    await member.send(
        f'Hello {member.name}, welcome to my Discord server!' 
    )

#Refreshes data retrieved from API 
def refresh_data():
    data = None
    while True:
        response = requests.get('https://catfact.ninja/fact?max_length=140')
        data = response.text
        parse_json = json.loads(data)
        active_case = parse_json['fact']
        return active_case

#
@client.event
async def on_message(message):
    if message.author == client.user:
        return 
        
    if client.user.mentioned_in(message):
        test()



client.run(TOKEN)