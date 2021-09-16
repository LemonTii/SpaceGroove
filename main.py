import discord
import os
from discord.channel import VoiceChannel
from dotenv import load_dotenv

client = discord.Client()
prefix = '!'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for: {}".format(prefix)))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith('{}'.format(prefix)):
        return

    if message.content.startswith('{}p '.format(prefix)) or message.content.startswith('{}play '.format(prefix)):
        await joinCall(message)
        await message.channel.send('play')
    
    elif message.content.startswith('{}skip'.format(prefix)) or message.content.startswith('{}next'.format(prefix)):
        await message.channel.send('skip')
    
    elif message.content.startswith('{}queue'.format(prefix)):
        await message.channel.send('show queue')
    
    elif message.content.startswith('{}remove '.format(prefix)):
        await message.channel.send('remove')

    elif message.content.startswith('{}leave'.format(prefix)):
        await leaveCall(message)
        await message.channel.send('leave')
    
    elif message.content.startswith('{}help'.format(prefix)):
        await message.channel.send('**Available Commands**:\n> {}play\n> {}skip\n> {}queue\n> {}remove\n> {}leave\n> {}help\n> {}changeprefix'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix))
    
    elif message.content.startswith('{}changeprefix '.format(prefix)):
        await changePrefix(message.content.strip('{}changeprefix '.format(prefix)))

    else:
        await message.channel.send('***{}*** is an unkown command. Use :help for a list of commands.'.format(message.content))

async def changePrefix(newPrefix):
    #needs variable change fix
    global prefix
    prefix = newPrefix
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for: {}".format(prefix)))

async def joinCall(message):
    voiceChannel = message.author.voice
    if not voiceChannel:
        return await message.channel.send("*You need to be connected to a voice channel!*")
    
    permissions = voiceChannel.channel.permissions_for(message.guild.me)
    if not permissions.connect or not permissions.speak:
        return await message.channel.send("*I can't join and play music without your permission!!*")
    
    await voiceChannel.channel.connect()

async def leaveCall(message):
    clientVoiceChannel = message.author.voice
    curVoiceChannel = message.guild

    if not clientVoiceChannel:
        return await message.channel.send("*You aren't even in a call...*")

    elif not curVoiceChannel:
        return await message.channel.send("*I'm not in a call. Don't bother me*")
    
    elif clientVoiceChannel.channel != curVoiceChannel.me.voice.channel:
        return await message.channel.send("***Gotta be in the same call as me!***")
    
    await curVoiceChannel.voice_client.disconnect()

load_dotenv()
client.run(os.getenv('TOKEN'))