import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import random
import datetime as dt
from artwork import rockets

client = discord.Client()

url = 'https://exogen.space/botapi/'
key = os.getenv("api_key")  # grabbing the API key
database = ['D8GM3S', 'token6']
target_server_id = 637447316856373268
target_channel_id = 741106877722656789
target_role_id = 741279442416173096

main_page = "https://exogen.space/"


def check_key(dictionary, k):
    if k in dictionary:
        return str(", " + dictionary[k])
    else:
        return ""


class Advisors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command to provide donor info
    @commands.command(
        pass_context=True,
        name="donor",
        description="Bot replies to sender in DM to verify registration as a donor in order to grant Advisor status.",
        help='initiates donor rewards process',
        usage="<token>"
    )
    async def donor(self, ctx, token='info'):
        if token == 'info':  # returning info about verifying donor status
            await asyncio.sleep(1)
            await ctx.author.send("Please go to the Exogen site and in the My Corporation panel on the left side "
                                  "and in the Manage My Corporation you will find your personal Donor token.\n"
                                  "For example: `A1B2C3`\n"
                                  "Enter it here and you will receive access to the secret channel!\n"
                                  "For example: `!donor A1B2C3`")
        elif not re.search(r"[a-zA-Z0-9]{6}", token):  # checking for token for format
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.author.send("**ERROR:** You need to enter a token in the correct format.")
        elif token not in database:  # checking if token not in database
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.author.send("**ERROR:** I'm sorry, but I cannot find this token in our database. "
                                      "Please try again in a few minutes (donation can be still processed) "
                                      "or contact us directly.")
        elif token in database:  # checking if token exists in database
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.author.send("Checking database.")
            async with ctx.typing():
                await asyncio.sleep(2)
                await ctx.author.send("Your token has been found.\nActivating donor rewards.")

            guild = self.bot.get_guild(target_server_id)
            channel = self.bot.get_channel(target_channel_id)
            role = guild.get_role(target_role_id)
            member = guild.get_member(ctx.message.author.id)

            if member:
                await member.add_roles(role)
                async with ctx.typing():
                    await asyncio.sleep(2)
                    await ctx.author.send("Congratulations {} and welcome to the {}'s channel {}!"
                                          .format(member.mention, role.name, channel.mention))
            else:
                async with ctx.typing():
                    await asyncio.sleep(1)
                    await ctx.author.send("You are not a member on this server.")

    # command to display Exogen stats
    @commands.command(
        pass_context=True,
        name="stats",
        description="Bot displays chosen Exogen stats",
        help='displays corp stats',
        usage="<All|Distance|Systems|Anomalies|Planets|SOS|Resources|Corps|Exogen>"
    )
    @commands.has_any_role('Server Booster', 'Pale Blue Dot', 'Advisor', 'Assistant', 'Supervisor', 'Manager')
    async def stats(self, ctx, stat="All"):
        xml_data = requests.get(main_page).content
        soup = BeautifulSoup(xml_data, "html.parser")
        stats = soup.select(".statsBox")
        all_stats = [string for string in stats[0].stripped_strings] \
            + [string for string in stats[1].stripped_strings] \
            + [string for string in stats[2].stripped_strings]
        exogen_stats = [
            dict(title=all_stats[0].title(), value=all_stats[1], system=all_stats[2], corp=all_stats[3]),
            dict(title=all_stats[4].title(), value=int(all_stats[5]), corp=all_stats[6]),
            dict(title=all_stats[7].title(), value=int(all_stats[8]), corp=all_stats[9]),
            dict(title=all_stats[10].title(), value=int(all_stats[11]), corp=all_stats[12]),
            dict(title=all_stats[13].title(), value=int(all_stats[14]), corp=all_stats[15]),
            dict(title=all_stats[16].title(), value=float(all_stats[17]), corp=all_stats[18]),
            dict(title=all_stats[19].title(), value=int(all_stats[20])),
            dict(title=all_stats[21].title(), value=int(all_stats[22])),
            dict(title=all_stats[23].title(), value=int(all_stats[24]), system=all_stats[25].title()),
            dict(title=all_stats[26].title(), value=int(all_stats[27]), system=all_stats[28].title()),
            dict(title=all_stats[29].title(), value=int(all_stats[30])),
            dict(title=all_stats[31].title(), value=int(all_stats[32])),
            dict(title=all_stats[33].title(), value=int(all_stats[34])),
            dict(title=all_stats[35].title(), value=int(all_stats[36])),
            dict(title=all_stats[37].title(), value=int(all_stats[38])),
            dict(title=all_stats[39].title(), value=all_stats[40]),
            dict(title=all_stats[41].title(), value=all_stats[42]),
            dict(title=all_stats[43].title(), value=int(all_stats[44].replace(' ', ''))),
            dict(title=all_stats[45].title(), value=int(all_stats[46].replace(' ', ''))),
            dict(title=all_stats[47].title(), value=int(all_stats[48].replace(' ', ''))),
            dict(title=all_stats[49].title(), value=int(all_stats[50].replace(' ', '')))
        ]
        async with ctx.typing():
            await asyncio.sleep(.5)
            await ctx.send("Let me check that for you, just a sec.")
        if stat == "All" or stat == "all":
            async with ctx.typing():
                await asyncio.sleep(3)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats]).replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="All Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)

        elif stat == "Distance" or stat == "distance":
            async with ctx.typing():
                await asyncio.sleep(.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[0]])\
                    .replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Distance Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Systems" or stat == "systems":
            async with ctx.typing():
                await asyncio.sleep(.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[1:12:10]]).replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Systems Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Anomalies" or stat == "anomalies":
            async with ctx.typing():
                await asyncio.sleep(.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[2:11:8]]).replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Anomalies Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Planets" or stat == "planets":
            async with ctx.typing():
                await asyncio.sleep(.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[3:13:9]]).replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Planets Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "SOS" or stat == "sos":
            async with ctx.typing():
                await asyncio.sleep(.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in [exogen_stats[4], exogen_stats[13], exogen_stats[14]]])\
                    .replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Small Orbital Station Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Resources" or stat == "resources":
            async with ctx.typing():
                await asyncio.sleep(1)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in [exogen_stats[5], exogen_stats[15], exogen_stats[16]]])\
                    .replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Resources Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Corps" or stat == "corps":
            async with ctx.typing():
                await asyncio.sleep(1.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[0:6]])\
                    .replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Corporation Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        elif stat == "Exogen" or stat == "exogen":
            async with ctx.typing():
                await asyncio.sleep(1.5)
                result = "\n".join(["**" + v["title"] + ":** " + str(v["value"]) + str(check_key(v, "system")) +
                                    str(check_key(v, "corp"))
                                    for v in exogen_stats[7:22]]).replace("'", "").replace('[', '').replace(']', '')
                payload = discord.Embed(
                    title="Collective Stats",
                    description=result,
                    colour=discord.Color.blue()
                )
                await ctx.send(embed=payload)
        else:
            async with ctx.typing():
                await asyncio.sleep(.5)
                await ctx.send("Please try again with a valid input. "
                               "If you need help try '!help stats' to see the usage and valid inputs.")



    # # @tasks.loop(seconds=60*60*24) # loop for checking donor status once per day

    # @tasks.loop(seconds=60*60*24)
    # async def donor_check(self, ctx):
    #     # receive the member ID/name from the event that looks up users that have stopped donating
    #     await ctx.member.send("Since it looks like you've disabled the donations you will be soon removed from the "
    #                           "donors channel. If you think that could be a mistake, please contact us at pm@t-h-m.com "
    #                           "as soon as possible. Thank you for your donations! It really means a lot for us!")
    #     await asyncio.sleep(60*5)
    #     guild = client.get_guild(id=target_server_id)
    #     role = ctx.guild.get_role(id=target_role_id)  # Test server Guild and Role IDs
    #     await member.remove_roles(role)

    # change this to a task as above
    @commands.command(
        pass_context=True,
        name='nodonor',
        help='checks if users are still donors',
        description='Bot will check server at least once per day and check for any users that are no longer listed in '
                    'the database as a donor. Then notify the user that they will be removed from the Advisors role '
                    'and channels, as well as provide contact info if they believe this to be an error.'
    )
    async def nodonor(self, ctx, member: discord.member):
        # receive the member ID/name from the event that looks up users that have stopped donating
        await ctx.member.send("Since it looks like you've disabled the donations you will be soon removed from the "
                              "donors channel. If you think that could be a mistake, please contact us at pm@t-h-m.com "
                              "as soon as possible. Thank you for your donations! It really means a lot for us!")
        await asyncio.sleep(60 * 5)
        guild = client.get_guild(id=target_server_id)
        role = ctx.guild.get_role(id=target_role_id)  # Test server Guild and Role IDs
        await member.remove_roles(role)

    @commands.command(
        pass_context=True,
        name='api',
        help='checks the api',
        description='Bot checks the api'
    )
    async def api(self, ctx, token='123abc', member='test'):
        if member == 'test':
            mid = "358287505256218624"
        else:
            mid = ctx.author.id
        data = {
            'SECRET_KEY': key,
            'DISCORD_ID': mid,
            'DONATION_TOKEN': token
        }
        post = requests.post(url, data)
        print(post.status_code)
        await ctx.send(post.status_code)

    @commands.command(
        name="blast_off",
        help="launches a rocket",
        description="Bot launches an ASCII art rocket.",
        aliases=['rocket']
    )
    @commands.has_any_role('Advisor', 'Assistant', 'Supervisor', 'Manager')
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def rocket(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(2)
            await ctx.send("```Rocket will be launching in T minus...```")
            await asyncio.sleep(0.1)
            await ctx.send("```5...```")
            await asyncio.sleep(1)
            await ctx.send("```4...```")
            await asyncio.sleep(1)
            await ctx.send("```3...```")
            await asyncio.sleep(1)
            await ctx.send("```2...```")
            await asyncio.sleep(1)
            await ctx.send("```1...```")
            await asyncio.sleep(1)
            await ctx.send(random.choice(rockets))
            await asyncio.sleep(2)
            await ctx.send("```Liftoff, we have liftoff!```")

    @rocket.error
    async def rocket_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'Rocket can be launched again {:.0f}h {:.0f}m {:.0f}s' \
                .format(error.retry_after // (60 * 60), (error.retry_after % 60 * 60) // 60, error.retry_after % 60)
            await ctx.send(msg)
        elif isinstance(error, commands.MissingPermissions):
            text = f"I'm sorry {ctx.message.author}, I can't let you do that."
            await ctx.send(ctx.message.channel, text)
        else:
            raise error

    # thanks donors on the 1st of every month, in the advisors channel
    @tasks.loop(hours=24)
    async def donor_thank(self, ctx):
        guild = self.bot.get_guild(target_server_id)
        channel = self.bot.get_channel(target_channel_id)
        role = guild.get_role(target_role_id)
        day = dt.date.today()
        embed = discord.Embed(title="A Glorious Dawn", url="https://youtu.be/zSgiXGELjbc",
                              description="A musical tribute to Carl Sagan and Stephen Hawking.",
                              color=discord.Color.dark_purple())
        if day.day == 1:
            await channel.send(f"{role.name} thank you for being a monthly Exogen donor, "
                               f"we're glad to have you chasing the glorious dawn with us.", embed=embed)

    @donor_thank.before_loop
    async def before_printer(self):
        print("Waiting for ready before starting donor thanks loop")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Advisors(bot))
