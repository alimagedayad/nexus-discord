import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Bot is ready")

client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')