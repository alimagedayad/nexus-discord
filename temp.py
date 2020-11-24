import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')