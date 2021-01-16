import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp
import requests
import json
import re
import os

# # grabbing the config file
# with open('config.json') as config_file:
#     secrets = json.load(config_file)


client = discord.Client()

url = 'https://exogen.space/botapi/'
key = os.getenv("api_key")  # grabbing the API key
database = ['D8GM3S', 'token6']
target_server_id = 637447316856373268
target_channel_id = 741106877722656789
target_role_id = 741279442416173096

rocket = r"""```
       !
       !
       ^
      / \
     /___\
    |=   =|
    |     |
    |     |
    |     |
    |     |
    |     |
    |     |
    |     |
    |     |
    |     |
   /|##!##|\
  / |##!##| \
 /  |##!##|  \
|  / ^ | ^ \  |
| /  ( | )  \ |
|/   ( | )   \|
    ((   ))
   ((  :  ))
   ((  :  ))
    ((   ))
     (( ))
      ( )
       .```"""


class Advisors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command to add user to a role
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

    # @tasks.loop(seconds=60*60*24) # loop for checking donor status once per day
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
        await asyncio.sleep(60*5)
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
    @commands.has_any_role('Assistant', 'Supervisor', 'Manager')
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
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
            await ctx.send(rocket)
            await asyncio.sleep(2)
            await ctx.send("```Liftoff, we have liftoff!```")

    @rocket.error
    async def rocket_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'Rocket can be launched again {:.0f}h {:.0f}m {:.0f}s'\
                .format(error.retry_after//(60*60), (error.retry_after%60*60)//60, error.retry_after%60)
            await ctx.send(msg)
        else:
            raise error


def setup(bot):
    bot.add_cog(Advisors(bot))
