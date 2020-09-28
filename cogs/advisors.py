import discord
from discord.ext import commands
import asyncio
import re

client = discord.Client()

database = ['D8GM3S', 'token6']
target_server_id = 704139386501201942
target_channel_id = 725386567740555416
target_role_id = 759941703066583072


class Advisors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command to add a user to a role
    @commands.command(
        pass_context=True,
        name="donor",
        description="Bot replies to sender in DM to initiate verification as a donor in order to grant Advisor status.",
        usage=""
    )
    async def donor(self, ctx):
        await asyncio.sleep(1)
        await ctx.author.send("Please go to the Exogen site and in the My Corporation panel on the left side "
                              "and in the Manage My Corporation you will find your personal Donor token.\n"
                              "For example: `D8GM3S`\n"
                              "Enter it here with the command `!token` and you will receive access to the secret "
                              "Advisors channels.\n"
                              "For example: `!token D8GM3S`")

    # command to add user to a role
    # @commands.command(
    #     pass_context=True,
    #     name="donor",
    #     description="Bot replies to sender in DM to verify registration as a donor in order to grant Advisor status.",
    #     usage="<token>"
    # )
    # async def donor(self, ctx, token='info'):
    #     if token == 'info':  # returning info about verifying donor status
    #         await asyncio.sleep(1)
    #         await ctx.author.send("Please go to the Exogen site and in the My Corporation panel on the left side "
    #                               "and in the Manage My Corporation you will find your personal Donor token.\n"
    #                               "For example: `D8GM3S`\n"
    #                               "Enter it here and you will receive access to the secret channel!\n"
    #                               "For example: `!donor D8GM3S`")
    #     elif not re.search(r"[a-zA-Z0-9]{6}", token):  # checking for token for format
    #         async with ctx.typing():
    #             await asyncio.sleep(1)
    #             await ctx.author.send("**ERROR:** You need to enter a token in the correct format.")
    #     elif token not in database:  # checking if token not in database
    #         async with ctx.typing():
    #             await asyncio.sleep(1)
    #             await ctx.author.send("**ERROR:** I'm sorry, but I cannot find this token in our database. "
    #                                   "Please try again in a few minutes (donation can be still processed) "
    #                                   "or contact us directly.")
    #     elif token in database:  # checking if token exists in database
    #         async with ctx.typing():
    #             await asyncio.sleep(1)
    #             await ctx.author.send("Checking database.")
    #         async with ctx.typing():
    #             await asyncio.sleep(2)
    #             await ctx.author.send("Your token has been found.\nActivating donor rewards.")
    #
    #         print(target_server_id)
    #
    #         # await client.wait_until_ready()
    #         # do stuff to check for token and add Advisor role in Exogen Discord server
    #         guild = client.get_guild(id=target_server_id)
    #         # channel = "#advisors_chat"
    #         channel = client.get_channel(id=target_channel_id)
    #         # role = "@Advisor"
    #         role = ctx.guild.get_role(id=target_role_id)
    #         member = guild.get_member(ctx.message.author.id)
    #         if member:
    #             await member.add_roles(role)
    #
    #         async with ctx.typing():
    #             await asyncio.sleep(2)
    #             # await ctx.author.send("Congratulations {} and welcome to the {}'s channel {}!"
    #             #                       .format(member.mention, role, channel))
    #             await ctx.author.send("Congratulations {} and welcome to the {}'s channel {}!"
    #                                   .format(member.mention, role.mention, channel.mention))

    # @client.event()  # event for checking donor status once per day

    @commands.command(
        pass_context=True,
        name='nodonor',
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


def setup(bot):
    bot.add_cog(Advisors(bot))
