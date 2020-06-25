from discord.ext import commands
from datetime import datetime as d
import numpy as np
import re


class Calculation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='distance',
        description='Command to measure distance between two systems, given their rad-Z coordinates',
        aliases=['d', 'dist'],
        usage='<rad-Z 1> <rad-Z 2>'
    )
    async def distance(self, ctx, coord1, coord2):

        # msg = ctx.message.content
        # prefix_used = ctx.prefix
        # alias_used = ctx.invoked_with
        # text = msg[len(prefix_used) + len(alias_used):]
        #
        if coord1 == '':
            await ctx.send(content="You need to list the first system's coordinates")
            pass
        elif coord2 == '':
            await ctx.send(content="You need to list the second system's coordinates")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord1):
            await ctx.send(content="You must enter the coordinates in the #####-##### format")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord2):
            await ctx.send(content="You must enter the coordinates in the #####-##### format")
            pass
        else:
            # await ctx.send('You sent {} and {} as the two systems to calculate distance.'.format(coord1, coord2))
            r1 = int(re.search(r"^\d{5}", coord1).group(0))
            z1 = int(re.search(r"\d{5}$", coord1).group(0))
            r2 = int(re.search(r"^\d{5}", coord2).group(0))
            z2 = int(re.search(r"\d{5}$", coord2).group(0))
            # await ctx.send("System 1's coords are R: {} and Z: {}"
            #                "\nSystem 2's coords are R: {} and Z: {}".format(r1, z1, r2, z2))
            dist = np.around(np.sqrt((np.square(z1) + np.square(z2)) -
                                     2 * (z1 * z2 * (np.cos(r1 / 10000 - r2 / 10000)))) / 10, 1)
            await ctx.send("The distance between {} and {} is {}JU".format(coord1, coord2, dist))

            pass

        return

    # @commands.command(
    #     name='',
    #     description=' command',
    #     aliases=[]
    # )
    # async def help_command(self, ctx, cog='all'):
    #     return


def setup(bot):
    bot.add_cog(Calculation(bot))
