from discord.ext import commands
import discord
import re

client = discord.Client()


class Advisors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command to add a user to a role
    @commands.command(
        pass_context=True,
        name="donor",
        description="Bot replies to sender in DM to verify registration as a donor in order to grant Advisor status.",
        usage="!donor <token>"
    )
    @commands.has_permissions(manage_roles=True)
    async def donor(self, ctx, token='info'):
        if token == 'info':  # returning info about verifying donor status
            await ctx.author.send("Please go to the Exogen site and in the My Corporation panel on the left side "
                                  "and in the Manage My Corporation you will find your personal Donor token.\n"
                                  "`For example: D8GM3S`\n"
                                  "Enter it here and you will receive access to the secret channel!\n"
                                  "`For example: !donor D8GM3S`")
        elif not re.search(r"[a-zA-Z0-9]{6}", token):  # checking for token for format
            await ctx.author.send("`***ERROR:*** You need to enter a token in the correct format.`")
        elif token in database:  # checking if token exists in database
            # do stuff to check for token and add Advisor role in Exogen Discord server
            role = discord.Role
            member = ctx.message.author
            await member.add_roles(role)
            channel = discord.CategoryChannel
            await ctx.author.send("Congratulations {} and welcome to the {}'s channel {}"
                                  .format(member.mention, role.mention, channel.mention))
        elif token not in database:  # checking if token not in database
            await ctx.author.send("```***ERROR:*** I'm sorry, but I cannot find this token in our database. "
                                  "Please try again in a few minutes (donation can be still processed) "
                                  "or contact us directly.```")

    @donor.error
    async def assign_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)


def setup(bot):
    bot.add_cog(Advisors(bot))
