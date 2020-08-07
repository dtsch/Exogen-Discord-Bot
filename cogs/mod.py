from discord.ext import commands
import discord

client = discord.Client()


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command info
    @commands.command(pass_context=True)
    # function that command runs
    async def add_role(ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.message.author
        await client.add_roles(member, role)


def setup(bot):
    bot.add_cog(Moderation(bot))
