import discord
from discord.ext import commands
verif = False
verif2 = False
verifcomplete = False
foundmail = False
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ".", intents=intents)
membertickets = [[],[]]
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

    await channel.send('Welcome to the official server for TKH Coventry University!!!\nFirst of all we need you to verify your tkh email address...\nplease enter `!!!verify youremail@tkh.edu.eg`')
    @client.event

    async def on_message(message):
        global verif
        global verif2
        global foundmail
        global verifcomplete
        global roles
        if message.author == client.user:
            return
        else:
            if message.content.startswith('!!!verify'):
                verif_code = '5911'
                msg = message.content
                msgcont = msg[10:]
                for letter in range(len(msgcont)):
                    if msgcont[letter] == '@':
                        foundmail = True
                        if msgcont[letter:] == '@tkh.edu.eg':
                            await channel.send(f'A verification code was sent to `{msgcont}`\nplease copy the code and type `!!!verify [verification code]`\nif you want to resend the email type `!!!verify resend`')
                            #send email 
                        else:
                            await channel.send(f'`{msgcont}` is not a TKH mail address...\nplease try again with a TKH email address')
                if msgcont == verif_code:
                    verif = True
                    await channel.send('You are now verified as a user\ntype `!!!verify roles`')
                elif msgcont == 'resend':
                    verif_code = '5911'
                    await channel.send('The verification code was resent to your email')
                elif msgcont == 'roles':
                    if verif == True:
                        verif2 = False
                        await channel.send('Please enter the number corresponding to the year you are in\n1) Foundation\n2) Year 1')
                        if msgcont == '1':
                            role = discord.utils.get(member.guild.roles, name="Foundation")
                            await member.add_roles(role)
                            verif2 = True
                            await channel.send('Please enter the number corresponding to the school you are in\n1) Design and media\n2) Engineering\n3) Computer science\n4) Business\n5) Psychology')
                        elif msgcont == '2':
                            role = discord.utils.get(member.guild.roles, name="Year 1")
                            await member.add_roles(role)
                            verif2 = True
                            await channel.send('Please enter the number corresponding to the school you are in\n1) Design and media\n2) Engineering\n3) Computer science\n4) Business\n5) Psychology')
                        elif verif2 == True:
                            if msgcont == '1':
                                role = discord.utils.get(member.guild.roles, name="Design & Media")
                                await member.add_roles(role)
                                role = discord.utils.get(member.guild.roles, name="Foundation")
                                if str(role) != "Foundation":
                                    await channel.send('Please enter the number corresponding to the major you are in\n1) Digital Media\n2) Graphic Design\n3) Interior Architecture & Design')
                                verifcomplete = True
                            elif msgcont == '2':
                                role = discord.utils.get(member.guild.roles, name="Engineering")
                                await member.add_roles(role)
                                role = discord.utils.get(member.guild.roles, name="Foundation")
                                if str(role) != "Foundation":
                                    await channel.send('Please enter the number corresponding to the major you are in\n1) Civil\n2) Mechanical\n3) Electrical & Electronics')
                                verifcomplete = True
                            elif msgcont == '3':
                                role = discord.utils.get(member.guild.roles, name="Computer Science")
                                await member.add_roles(role)
                                role = discord.utils.get(member.guild.roles, name="Foundation")
                                if str(role) != "Foundation":
                                    await channel.send('Please enter the number corresponding to the major you are in\n1) Comp. Sci.\n2) Computing\n3) Cyber Security & Ethical Hacking')
                                verifcomplete = True
                            elif msgcont == '4':
                                role = discord.utils.get(member.guild.roles, name="Business")
                                await member.add_roles(role)
                                role = discord.utils.get(member.guild.roles, name="Foundation")
                                verifcomplete = True
                            elif msgcont == '5':
                                role = discord.utils.get(member.guild.roles, name="Psychology")
                                await member.add_roles(role)
                                verifcomplete = True
                    elif verifcomplete == True:
                        role = discord.utils.get(member.guild.roles, name="Waiting for verification")
                        await member.remove_roles(role)
                    else:
                        await channel.send('you are not verified yet')
                else:
                    if foundmail == True:
                        pass
                    else:
                        await channel.send('Please enter a valid command')
                    
        
@client.event
async def on_member_remove(member):
    #if member not verified delete the channel that is with their name
    role = discord.utils.get(member.guild.roles, name="Waiting for verification")
    if str(role) == "Waiting for verification":
        for i in range(len(membertickets[1])):
            if membertickets[1][i] == member:
                # await  member.guild.delete_text_channel(membertickets[0][i])
                await membertickets[0][i].delete()
    print(f"{member} has left the server")


client.run('NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U')