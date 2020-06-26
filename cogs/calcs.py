from discord.ext import commands
import datetime as dt
import numpy as np
import re


class Calculation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='distance',
        description='Command to measure distance between two systems, given their rad-Z coordinates',
        aliases=['d'],
        usage='<rad-Z 1> <rad-Z 2>'
    )
    async def distance(self, ctx, coord1, coord2):
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
            r1 = int(re.search(r"^\d{5}", coord1).group(0))
            z1 = int(re.search(r"\d{5}$", coord1).group(0))
            r2 = int(re.search(r"^\d{5}", coord2).group(0))
            z2 = int(re.search(r"\d{5}$", coord2).group(0))
            dist = np.around(np.sqrt((np.square(z1) + np.square(z2)) -
                                     2 * (z1 * z2 * (np.cos((r1 - r2) / 10000)))) / 10, 1)
            await ctx.send("The distance between {} and {} is {}JU".format(coord1, coord2, dist))
            pass
        return

    @commands.command(
        name='missions',
        description='Command to calculate mission times to a system in "<days>, hh:mm:ss" format, '
                    'along with associated costs',
        aliases=['m'],
        usage='<rad-Z> <# of stars+planets> <Subroutine Scanner upgrade (T/F)>'
    )
    async def mission(self, ctx, coord, bodies=0, upgrade=False):
        if coord == '':
            await ctx.send(content="You need to list the system's coordinates")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord):
            await ctx.send(content="You must enter the coordinates in the #####-##### format")
            pass
        elif not isinstance(bodies, int):
            await ctx.send(content="You must enter the # of stars and planets as an integer")
            pass
        else:
            # r = int(re.search(r"^\d{5}", coord).group(0))
            z = int(re.search(r"\d{5}$", coord).group(0))
            z_hours = np.floor(z/10)
            probe_time = dt.timedelta(hours=int(z_hours + np.floor(bodies/2)),
                                      minutes=int(((z/10) - z_hours) * 60 + (bodies % 2) * 30))
            # probe_hours = int(z_hours + b_hours)
            # probe_mins = int(((z/10) - z_hours) * 60 + (bodies % 2) * 30)
            pioneer_time = dt.timedelta(hours=int(z_hours + 6), minutes=int(((z/10) - z_hours) * 60))
            # pioneer_hours = int(z_hours + 6)
            # pioneer_mins = int(((z/10) - z_hours) * 60)
            pioneer_xe = np.ceil(z/10) * 0.1
            if upgrade:
                pioneer_w = 2
            else:
                pioneer_w = 3
            fs_time = dt.timedelta(hours=int(z_hours), minutes=int(((z/10) - z_hours) * 60))
            # fs_hours = int(z_hours)
            # fs_mins = int(((z/10) - z_hours) * 60)
            fs_xe = (np.ceil(z/10) * 0.2) + 1
            sos_time = dt.timedelta(hours=int(z_hours + 6), minutes=int(((z/10) - z_hours) * 60))
            # sos_hours = int(z_hours + 6)
            # sos_mins = int(((z/10) - z_hours) * 60)
            sos_xe = (np.ceil(z/10) * 0.3) + 3
            await ctx.send("A probe to {} will take {} and cost 3 Plasteel\n"
                           "A pioneer to {} will take {} and cost {} Xe, {} Water, 2 Plasteel\n"
                           "A fuel station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 3 Plasteel\n"
                           "A small orbital station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, "
                           "1 Plasteel, 10 Licenses"
                           .format(coord, str(probe_time),
                                   coord, str(pioneer_time), pioneer_xe, pioneer_w,
                                   coord, str(fs_time), fs_xe,
                                   coord, str(sos_time), sos_xe))
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
