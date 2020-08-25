from discord.ext import commands
import discord

client = discord.Client()


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mod_fcn(self, ctx): pass # add some function here


def setup(bot):
    bot.add_cog(Moderation(bot))
