import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix=".", intents=intents)
membertickets = [[], [], [], [], []]
# [memberdata],[email],[verification status],[verification channel],[]

verif = 0


@client.event
async def on_ready():
    print("Bot is ready")



@client.command()
@commands.has_role('Waiting for verification')
async def verify(ctx, arg, reply):
    if arg == 'roles':
        message = await ctx.channel.send("React to me!")
        await message.add_reaction(emoji="🔴")
        await message.add_reaction(emoji="🔵")

        @client.event
        async def on_reaction_add(reaction, member):
            rolesdone = False
            message2 = ''
            message3 = ''
            if member == client.user:
                return
            else:

                if reaction.message == message:
                    rolesdone = False
                    if reaction.emoji == "🔴":
                        role = discord.utils.get(ctx.guild.roles, name="Foundation")
                        message2 = await ctx.channel.send("React to me!")
                        await message2.add_reaction(emoji="🔴")
                        await message2.add_reaction(emoji="🔵")
                        await message2.add_reaction(emoji="⚪")
                        await message2.add_reaction(emoji="🟡")
                        await message2.add_reaction(emoji="🟢")
                    if reaction.emoji == "🔵":
                        role = discord.utils.get(ctx.guild.roles, name="Year 1")
                        message3 = await ctx.channel.send("React to me!")
                        await message3.add_reaction(emoji="🔴")
                        await message3.add_reaction(emoji="🔵")
                        await message3.add_reaction(emoji="⚪")
                elif reaction.message == message2:
                    if reaction.emoji == "🔴":
                        role2 = discord.utils.get(ctx.guild.roles, name="Computer Science")
                        rolesdone = True
                    if reaction.emoji == "🔵":
                        role2 = discord.utils.get(ctx.guild.roles, name="Engineering")
                        rolesdone = True
                    if reaction.emoji == "⚪":
                        role2 = discord.utils.get(ctx.guild.roles, name="Design & Media")
                        rolesdone = True
                    if reaction.emoji == "🟡":
                        role2 = discord.utils.get(ctx.guild.roles, name="Business")
                        rolesdone = True
                    if reaction.emoji == "🟢":
                        role2 = discord.utils.get(ctx.guild.roles, name="Psychology")
                        rolesdone = True
                elif reaction.message == message3:
                    if reaction.emoji == "🔴":
                        role2 = discord.utils.get(ctx.guild.roles, name="Computer Science")
                        rolesdone = True
                    if reaction.emoji == "🔵":
                        role2 = discord.utils.get(ctx.guild.roles, name="Engineering")
                        rolesdone = True
                    if reaction.emoji == "⚪":
                        role2 = discord.utils.get(ctx.guild.roles, name="Design & Media")
                        rolesdone = True
                if rolesdone:
                    await member.add_roles(role, role2)


client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')