import os 
import requests 
from discord.ext import commands
import discord 
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
intents=discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    # guild = discord.utils.find(lambda g: g.name == SERVER, client.guilds)
    
    guild = discord.utils.get(client.guilds, name=SERVER)

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}')

@client.event 
async def on_member_join(member):
    guild = client.get_guild(1103430473633513658)
    channel = guild.get_channel(1103430474338152545)
    await channel.send(f'Welcome to the server {member.mention}!  ')
    await member.create_dm()
    await member.send(
        f'Hello {member.name}, welcome to my Discord server!' 
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    
    if client.user.mentioned_in(message):
        await message.channel.send('Hello')


client.run(TOKEN)