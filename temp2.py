import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ".", intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")
    role = discord.utils.get(member.guild.roles, name="Waiting for verification")
    await member.add_roles(role)
    name = 'New member verification'
    category = discord.utils.get(member.guild.categories, name=name)

    channel = await member.guild.create_text_channel(f'Welcome {member.name}', category=category)
    await channel.set_permissions(member, read_messages=True,
                                                      send_messages=True,
                                                      read_message_history=True)

    await channel.send('Hello!')
    
@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")


client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')