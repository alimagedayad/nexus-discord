import discord
from discord.ext import commands
import uuid
import os
from time import sleep
from discord.utils import get
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
membertickets = [[], [], []]

cred = credentials.Certificate(
    {
        "type": os.environ["accountType"],
        "project_id": os.environ.get("projectID"),
        "private_key_id": "3223e5adfefa6379f93830531d3fdeb271a1071c",
        "private_key": os.environ.get("privateKey"),
        "client_email": os.environ.get("clientEmail"),
        "client_id": os.environ.get("clientID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("clientX509CertUrl"),
    }
)
# print()
# firebase_admin.initialize_app({credential})


firebase_admin.initialize_app(
    cred,
    {"databaseURL": "https://tkh-nexus-discord.firebaseio.com"},
)


db = firestore.client()
verif = 0
sg_api = os.environ.get("sendgridApi")


def build_hello_email(to, subject):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
        from_email="verification@ayad.xyz",
        to_emails=to,
        subject=subject,
        html_content=f"Hey!, <br> Your <strong>{subject}</strong>",
    )
    try:
        sendgrid_client = SendGridAPIClient(sg_api)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def saveUIDinDB(userID, token, roles):
    doc_ref = db.collection("users").document(str(userID))
    role_names = [role.name for role in roles][1:]
    roles = ",".join(role_names)
    doc_ref.set({"id": userID, "token": token, "roles": roles, "verified": False})


try:

    @client.event
    async def on_ready():
        print("Bot is ready!")

    def not_bot_reaction(reaction, user):
        return user != client.user

    orMessage = ""

    @client.event
    async def on_member_join(member):
        print(f"{member} has joined the server")
        role = discord.utils.get(member.guild.roles, name="Waiting for verification")
        await member.add_roles(role)
        name = "New member verification"
        category = discord.utils.get(member.guild.categories, name=name)

        channel = await member.guild.create_text_channel(
            f"Welcome {member.name}", category=category
        )
        membertickets[0].append(channel)
        membertickets[1].append(member)
        await channel.set_permissions(
            member, read_messages=True, send_messages=True, read_message_history=True
        )

        await channel.send(
            "Welcome to the official server for TKH Coventry University!!!\nFirst of all we need you to verify your tkh email address...\nplease enter `.verify email youremail@tkh.edu.eg`"
        )

    @client.event
    async def on_member_remove(member):
        # if member not verified delete the channel that is with their name
        role = discord.utils.get(member.guild.roles, name="Waiting for verification")
        if str(role) == "Waiting for verification":
            for i in range(len(membertickets[1])):
                if membertickets[1][i] == member:
                    await membertickets[0][i].delete()
        print(f"{member} has left the server")

    @client.command()
    # @commands.has_role("Waiting for verification")
    async def verify(ctx, arg, reply):
        # try:
        role_names = [role.name for role in ctx.message.author.roles][1:]
        if "Waiting for verification" in role_names:
            if arg == "email":
                regex = "[^@]+@[^@]+\.[^@]+"
                res = reply[reply.index("@") + 1 :]
                if re.search(regex, reply):
                    if res == "tkh.edu.eg":
                        verifyCode = uuid.uuid4().hex[
                            :4
                        ]  # Might reduce uniqueness because of slicing
                        saveUIDinDB(
                            ctx.message.author.id, verifyCode, ctx.message.author.roles
                        )
                        build_hello_email(reply, f"verification code is {verifyCode}")
                        await ctx.send(f"The verification code was sent to {reply}!")
                        await ctx.send(
                            f"To verify your account send ```.verify code your_verification_code```"
                        )
                    else:
                        await ctx.send(f"Invalid domain")
                else:
                    await ctx.send(f"This email {reply} is invalid")
            elif arg == "code":
                userID = ctx.message.author.id
                token = reply
                try:
                    # role, role1, role2, role3 = None
                    docs = db.collection("users").where("id", "==", userID).stream()
                    stream_empty = True
                    for doc in docs:
                        stream_empty = False
                        userDict = doc.to_dict()

                        if userDict["verified"] == True:
                            await ctx.send(f"You're account is already verified!")
                            break

                        if userDict["token"] == token:
                            doc_ref = db.collection("users").document(str(userID))
                            doc_ref.update({"verified": True})

                            member = ctx.message.author
                            await ctx.send(f"0️⃣ = Year 0 (Foundation)\n1️⃣ = Year 1")
                            message = await ctx.send("In which year you're in?")
                            await message.add_reaction(emoji="0️⃣")
                            await message.add_reaction(emoji="1️⃣")

                            def check(reaction, user):
                                emojis = [
                                    "0️⃣",
                                    "1️⃣",
                                    "💻",
                                    "📐",
                                    "🎨",
                                    "💹",
                                    "😄",
                                    "🔥",
                                    "🖱️",
                                    "⌨️",
                                    "⚡",
                                    "🚧",
                                    "🚗",
                                    "🧑‍🎨",
                                    "😎",
                                    "🤑",
                                    "🕴",
                                    "💁‍♂️",
                                    "🥰",
                                ]
                                return (
                                    str(reaction.emoji) in emojis
                                    and user != client.user
                                )

                            reaction, user = await client.wait_for(
                                "reaction_add", check=check
                            )

                            if str(reaction.emoji) == "0️⃣":
                                role = discord.utils.get(
                                    member.guild.roles, name="Foundation"
                                )
                            elif str(reaction.emoji) == "1️⃣":
                                role = discord.utils.get(
                                    member.guild.roles, name="Year 1"
                                )
                            if role:
                                await ctx.send(
                                    f"💻 = School of Computing \n📐 = School of Engineering\n🎨 = School of Media and Design\n💹 = School of Business\n😄 = School of Psychology"
                                )
                                message2 = await ctx.send("Which School:")
                                await message2.add_reaction(emoji="💻")
                                await message2.add_reaction(emoji="📐")
                                await message2.add_reaction(emoji="🎨")
                                await message2.add_reaction(emoji="💹")
                                await message2.add_reaction(emoji="😄")

                                reaction, user = await client.wait_for(
                                    "reaction_add", check=check
                                )

                                if str(reaction.emoji) == "💻":
                                    role2 = discord.utils.get(
                                        member.guild.roles, name="Computing"
                                    )
                                elif str(reaction.emoji) == "📐":
                                    role2 = discord.utils.get(
                                        member.guild.roles, name="Engineering"
                                    )
                                elif str(reaction.emoji) == "🎨":
                                    role2 = discord.utils.get(
                                        member.guild.roles, name="Design & Media"
                                    )
                                elif str(reaction.emoji) == "💹":
                                    role2 = discord.utils.get(
                                        member.guild.roles, name="Business"
                                    )
                                elif str(reaction.emoji) == "😄":
                                    role2 = discord.utils.get(
                                        member.guild.roles, name="Psychology"
                                    )

                                if role and role2:
                                    message3 = await ctx.send("Which major?")
                                    if str(role2) == "Computing":
                                        await message3.add_reaction(emoji="🔥")
                                        await message3.add_reaction(emoji="🖱️")
                                        await message3.add_reaction(emoji="⌨️")
                                        desc = await ctx.send(
                                            f"🔥 = Ethical Hacking & Cybersecurity \n🖱️ = Computing \n⌨️ = Computer Science"
                                        )

                                    elif str(role2) == "Engineering":
                                        await message3.add_reaction(emoji="⚡")
                                        await message3.add_reaction(emoji="🚧")
                                        await message3.add_reaction(emoji="🚗")
                                        desc = await ctx.send(
                                            f"⚡ = Electrical and Electronic  \n🚧 = Civil \n🚗 = Mechanical"
                                        )
                                    elif str(role2) == "Design & Media":
                                        await message3.add_reaction(emoji="🖥️")
                                        await message3.add_reaction(emoji="🧑‍🎨")
                                        await message3.add_reaction(emoji="🎨")
                                        desc = await ctx.send(
                                            f"🖥️ = Digital Media  \n👨‍🎨 = Interior Architecture \n 🎨 = Graphic Design"
                                        )
                                    elif str(role2) == "Business":
                                        await message3.add_reaction(emoji="😎")
                                        await message3.add_reaction(emoji="🤑")
                                        await message3.add_reaction(emoji="🕴")
                                        await message3.add_reaction(emoji="💁‍♂️")
                                        desc = await ctx.send(
                                            f"😎 = Business and HR  \n🤑 = Accounting and Finance \n💁‍♂️ = Business and Marketing \n🕴️ = Business Administration"
                                        )

                                    elif str(role2) == "Psychology":
                                        await ctx.send(f"🥰 = Psychology")
                                        desc = await message3.add_reaction(emoji="🥰")

                                    reaction3, usery = await client.wait_for(
                                        "reaction_add", check=check
                                    )

                                    if str(reaction3) == "🔥":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Ethical Hacking & Cybersecurity",
                                        )
                                    elif str(reaction3) == "🖱️":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Computing"
                                        )
                                    elif str(reaction3) == "⌨️":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Computer Science"
                                        )
                                    elif str(reaction3) == "⚡":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Electrical & Electronics",
                                        )
                                    elif str(reaction3) == "🚧":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Civil"
                                        )
                                    elif str(reaction3) == "🚗":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Mechanical"
                                        )
                                    elif str(reaction3) == "🖥️":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Digital Media"
                                        )
                                    elif str(reaction3) == "👨‍🎨":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Interior Architecture & Design",
                                        )
                                    elif str(reaction3) == "🎨":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Graphic Design"
                                        )
                                    elif str(reaction3) == "😎":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Business & HR Management",
                                        )
                                    elif str(reaction3) == "🤑":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Accounting & Finance",
                                        )
                                    elif str(reaction3) == "💁‍♂":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Business and Marketing",
                                        )
                                    elif str(reaction3) == "️🕴":
                                        role3 = discord.utils.get(
                                            member.guild.roles,
                                            name="Business Administration",
                                        )
                                    elif str(reaction3) == "🥰":
                                        role3 = discord.utils.get(
                                            member.guild.roles, name="Psychology"
                                        )

                                    # await ctx.send(f'roles: #1{role} #2{role2} #3{role3}')
                                    # await ctx.send('.....')
                                    # await message.delete()
                                    # await message2.delete()
                                    # await message3.delete()
                                    # await desc.delete()

                                    await member.add_roles(role, role2, role3)
                                    await member.remove_roles(
                                        discord.utils.get(
                                            member.guild.roles,
                                            name="Waiting for verification",
                                        )
                                    )
                                    await ctx.send(
                                        f"Congrats <@{userID}>! Your account is verified now! \n Welcome abroad!"
                                    )
                    if stream_empty:
                        await ctx.send(
                            "Please try again and if the issue persists contact our support team on nexus@tkh.edu.eg"
                        )
                except Exception as e:
                    print("Oops!. Catched!!: ", e)
        else:
            await ctx.send("Your account is already verified!")

    # except:
    #     pass
    # await ctx.send(f"'arg: ', {arg}, 'reply:', {reply}")

    @client.command()
    async def fs(ctx, arg):
        if arg == "test":
            await ctx.send("Test!")

    # @client.command()
    # @commands.has_role("Waiting for verification")
    # async def oldverify(ctx, arg, reply):
    #     global verif
    #     vercode = "5911"
    #     if arg == "email":
    #         for letter in range(len(reply)):
    #             if reply[letter] == "@":
    #                 if reply[letter:] == "@tkh.edu.eg":
    #                     await ctx.channel.send(
    #                         f"A verification code was sent to `{reply}`\nplease copy the code and type `.verifycode [verification code]`\nif you want to resend the email type `!!!verify resend`"
    #                     )
    #                     # send email
    #
    #                 else:
    #                     await ctx.channel.send(
    #                         f"`{reply}` is not a TKH mail address...\nplease try again with a TKH email address"
    #                     )
    #     elif arg == "code":
    #         if verif == 1:
    #             await ctx.channel.send("You are already verified")
    #         elif vercode == reply:
    #             verif = 1
    #             await ctx.channel.send(
    #                 "You are now verified as a user\ntype `!!!verify roles`"
    #             )
    #         elif reply == "resend":
    #             await ctx.channel.send("The verification code was resent to your email")

    client.run("NjQyMzE2NTk4Mzk2MzIxNzky.XcVJ8g.ND51DUv_gcqmHWrrkwNwOqC3n5U")


except Exception as e:
    print("exception: ", e)
