import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ".", intents=intents)
membertickets = [[],[],[]]
# [memberdata],[email],[verification status]

verif = 0
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
    membertickets[0].append(channel)
    membertickets[1].append(member)
    await channel.set_permissions(member, read_messages=True,
                                                      send_messages=True,
                                                      read_message_history=True)

    await channel.send('Welcome to the official server for TKH Coventry University!!!\nFirst of all we need you to verify your tkh email address...\nplease enter `.verify email youremail@tkh.edu.eg`')

@client.event
async def on_member_remove(member):
    #if member not verified delete the channel that is with their name
    role = discord.utils.get(member.guild.roles, name="Waiting for verification")
    if str(role) == "Waiting for verification":
        for i in range(len(membertickets[1])):
            if membertickets[1][i] == member:
                await membertickets[0][i].delete()
    print(f"{member} has left the server")

@client.command()
@commands.has_role('Waiting for verification')
async def verify(ctx, arg, reply):
    global verif
    vercode = '5911'
    if arg == 'email':
        for letter in range(len(reply)):
            if reply[letter] == '@':
                if reply[letter:] == '@tkh.edu.eg':
                    await ctx.channel.send(f'A verification code was sent to `{reply}`\nplease copy the code and type `.verifycode [verification code]`\nif you want to resend the email type `!!!verify resend`')
                    #send email 
                    
                else:
                    await ctx.channel.send(f'`{msgcont}` is not a TKH mail address...\nplease try again with a TKH email address')
    elif arg == 'code':
        if verif == 1:
            await ctx.channel.send('You are already verified')
        elif vercode == reply:
            verif = 1
            await ctx.channel.send('You are now verified as a user\ntype `!!!verify roles`')
        elif reply == 'resend':
            await ctx.channel.send('The verification code was resent to your email')
    

client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')