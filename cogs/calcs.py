from discord.ext import commands
import datetime as dt
import numpy as np
import re


class Calculation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command info
    @commands.command(
        name='distance',
        description='Command to measure distance between two systems, given their rad-Z coordinates',
        aliases=['d', 'dz', 'd1'],
        usage='<rad-Z 1> <rad-Z 2>'
    )
    # function that command runs
    async def distance(self, ctx, coord1, coord2):
        if coord1 == '':  # checking for blank arg
            await ctx.send(content="`You need to list the first system's coordinates.`")
            pass
        elif coord2 == '':  # checking for blank arg
            await ctx.send(content="`You need to list the second system's coordinates.`")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord1):  # checking for arg format
            await ctx.send(content="`You must enter the coordinates in the #####-##### format.`")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord2):  # checking for arg format
            await ctx.send(content="`You must enter the coordinates in the #####-##### format.`")
            pass
        else:  # if passes checks, parses args for calculation
            r1 = int(re.search(r"^\d{5}", coord1).group(0))
            z1 = int(re.search(r"\d{5}$", coord1).group(0))
            r2 = int(re.search(r"^\d{5}", coord2).group(0))
            z2 = int(re.search(r"\d{5}$", coord2).group(0))
            dist = np.around(np.sqrt((np.square(z1) + np.square(z2)) -
                                     2 * (z1 * z2 * (np.cos((r1 - r2) / 10000)))) / 10, 1)
            await ctx.send("`The distance between {} and {} is {}JU.`".format(coord1, coord2, dist))
            pass
        return

    # command info
    @commands.command(
        name='missions',
        description='Command to calculate mission times to a system in "<days>, hh:mm:ss" format, '
                    'along with associated costs',
        aliases=['m', 'mz', 'm1'],
        usage='<rad-Z> <# of stars+planets> <Mission (All, Probe, PB, Pioneer, PN, Fuel Station, FS, '
              'Small Orbital Station, SOS, Science Vessel, SV, Mining Operation, MO> '
              '<Subroutine Scanner upgrade (True/False)> <Augmented Workforce upgrade (True/False)> '
              'Subroutine Mining Drones upgrade (True/False)'
    )
    # function that command runs
    async def mission(self, ctx, coord, bodies=1, mission="All", ss=False, aw=False, smd=False):
        if coord == '':  # checking for blank arg
            await ctx.send(content="`You need to list the system's coordinates`")
            pass
        elif not re.search(r"\d{5}-\d{5}", coord):  # checking for arg format
            await ctx.send(content="`You must enter the coordinates in the #####-##### format`")
            pass
        elif not isinstance(bodies, int):  # checking for arg format
            await ctx.send(content="`**ERROR:** You must enter the # of stars and planets as an integer`")
            pass
        else:  # if passes checks, parses args for calculation
            # r = int(re.search(r"^\d{5}", coord).group(0))
            z = int(re.search(r"\d{5}$", coord).group(0))
            z_hours = np.floor(z / 10)
            probe_time = dt.timedelta(hours=int(z_hours + np.floor(bodies / 2)),
                                      minutes=int(((z / 10) - z_hours) * 60 + (bodies % 2) * 30))
            pioneer_time = dt.timedelta(hours=int(z_hours + 6), minutes=int(((z / 10) - z_hours) * 60))
            pioneer_xe = np.ceil(z / 10) * 0.1
            if ss:  # checks if player set upgrade value to T, may need to make this more robust
                pioneer_w = 2
            else:
                pioneer_w = 3
            fs_time = dt.timedelta(hours=int(z_hours), minutes=int(((z / 10) - z_hours) * 60))
            fs_xe = (np.ceil(z / 10) * 0.2) + 1
            sos_time = dt.timedelta(hours=int(z_hours + 6), minutes=int(((z / 10) - z_hours) * 60))
            sos_xe = (np.ceil(z / 10) * 0.3) + 3
            sv_time = fs_time + dt.timedelta(hours=72)
            sv_xe = (np.ceil(z / 10) * 0.2) + 1  # will have to check if system is anomaly once connected to server
            if smd:
                mo_time = fs_time + dt.timedelta(hours=192)
            else:
                mo_time = fs_time + dt.timedelta(hours=168)

            mo_xe = (np.ceil(z / 10) * 0.3) + 1
            if aw:
                mo_ore = 0
            else:
                mo_ore = 5

        if mission == 'All':
            await ctx.send("```A Probe to {} will take {} and cost 3 Plasteel\n"
                           "A Pioneer to {} will take {} and cost {} Xe, {} Water, 2 Plasteel.\n"
                           "A Fuel Station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 3 Plasteel.\n"
                           "A Small Orbital Station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 1 Plasteel, "
                           "10 Licenses.\n"
                           "A Science Vessel to {} will take {} and cost {} Xe, 3 Water, 1 Ore, 10 Plasteel, "
                           "10 Licenses.\n"
                           "A Mining Operation to {} will take {} and cost {} Xe, 5 Water, 5 Ore, 5 Plasteel, "
                           "5 Licenses.```"
                           .format(coord, str(probe_time)
                                   , coord, str(pioneer_time), pioneer_xe, pioneer_w
                                   , coord, str(fs_time), fs_xe
                                   , coord, str(sos_time), sos_xe
                                   , coord, str(sv_time), sv_xe
                                   , coord, str(mo_time), mo_xe))
        elif mission == 'Probe' or mission == 'PB':
            await ctx.send("```A Probe to {} will take {} and cost 3 Plasteel```".format(coord, str(probe_time)))
        elif mission == 'Pioneer' or mission == 'PN':
            await ctx.send("```A Pioneer to {} will take {} and cost {} Xe, {} Water, 2 Plasteel.```"
                           .format(coord, str(pioneer_time), pioneer_xe, pioneer_w))
        elif mission == 'Fuel Station' or mission == 'FS':
            await ctx.send("```A Fuel Station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 3 Plasteel.```"
                           .format(coord, str(fs_time), fs_xe))
        elif mission == 'Small Orbital Station' or mission == 'SOS':
            await ctx.send("```A Small Orbital Station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 1 Plasteel, "
                           "10 Licenses.```".format(coord, str(sos_time), sos_xe))
        elif mission == 'Science Vessel' or mission == 'SV':
            await ctx.send(
                "```A Science Vessel to {} will take {} and cost {} Xe, 3 Water, 1 Ore, 10 Plasteel, 10 Licenses.```"
                .format(coord, str(sv_time), sv_xe))
        elif mission == 'Mining Operation' or mission == 'MO':
            await ctx.send(
                "```A Mining Operation to {} will take {} and cost {} Xe, 5 Water, {} Ore, 5 Plasteel, 5 Licenses.```"
                .format(coord, str(mo_time), mo_xe, mo_ore))
        else:
            await ctx.send(content="```***ERROR*** You must enter a viable mission type, abbreviation, or 'All'.```")


        # await ctx.send("```A probe to {} will take {} and cost 3 Plasteel.\n"
        #                "A pioneer to {} will take {} and cost {} Xe, {} Water, 2 Plasteel.\n"
        #                "A fuel station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, 3 Plasteel.\n"
        #                "A small orbital station to {} will take {} and cost {} Xe, 3 Water, 3 Ore, "
        #                "1 Plasteel, 10 Licenses.\n"
        #                "A science vessel to {} will take {} and cost {} Xe, 3 Water, 1 Ore, 10 Plasteel, "
        #                "10 Licenses.\n"
        #                "A mining operation to {} will take {} and cost {} Xe, 5 Water, 5 Ore, 5 Plasteel, "
        #                "5 Licenses.```"
        #                .format(coord, str(probe_time),
        #                        coord, str(pioneer_time), pioneer_xe, pioneer_w,
        #                        coord, str(fs_time), fs_xe,
        #                        coord, str(sos_time), sos_xe,
        #                        coord, str(sv_time), sv_xe,
        #                        coord, str(mo_time), mo_xe))
            pass

        return


def setup(bot):
    bot.add_cog(Calculation(bot))
