from discord.ext import commands
import datetime as dt
import numpy as np
import re


class Calculation2(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command info
    # noinspection PyUnboundLocalVariable,PyShadowingNames
    @commands.command(
        name='missions_e',
        description='Command to calculate mission times to a system in "<days>, hh:mm:ss" format, '
                    'along with associated costs',
        aliases=['me1'],
        usage='<rad-Z> <# of stars+planets> <Mission (All, Prob/PB, Pioneer/PN, Fuel Station/FS, '
              'Small Orbital Station/SOS, Science Vessel/SV, Mining Operation/MO, Lunar Base/LB)> '
              '<Subroutine Scanner upgrade (True/False)> <Augmented Workforce upgrade (True/False)> '
              'Subroutine Mining Drones upgrade (True/False)'
    )
    @commands.dm_only()
    # function that command runs
    async def mission_e(self, ctx, coord, bodies=1, mission="All", ss=False, aw=False, smd=False):
        if coord == '':  # checking for blank arg
            await ctx.send("`***ERROR:*** You need to list the system's coordinates`")
        elif not re.search(r"\d{5}-\d{5}", coord):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the coordinates in the #####-##### format`")
        elif not isinstance(bodies, int):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the # of stars and planets as an integer`")
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
            lb_time = fs_time + dt.timedelta(hours=168)
            lb_xe = (np.ceil(z / 10) * 1)

        if mission == 'All':
            await ctx.send("A Probe :Probe: to {} will take {} and cost 3 :Plasteel:\n"
                           "A Pioneer :Pioneer: to {} will take {} and cost {} :Xe:, {} :Water:, 2 :Plasteel:.\n"
                           "A Fuel Station :FuelStation: to {} will take {} and cost {} :Xe:, 3 :Water:, 3 :Ore:, "
                           "3 :Plasteel:.\n"
                           "A Small Orbital Station :SmallOrbitalStation: to {} will take {} and cost {} :Xe:, "
                           "3 :Water:, 3 :Ore:, 1 :Plasteel:, 10 :License:.\n"
                           "A Science Vessel :ScienceVessel: to {} will take {} and cost {} :Xe:, 3 :Water:, 1 :Ore:, "
                           "10 :Plasteel:, 10 :License:.\n"
                           "A Mining Operation :MiningOperation: to {} will take {} and cost {} :Xe:, 5 :Water:, "
                           "{} :Ore:, 5 :Plasteel:, 5 :License:.\n"
                           "A Lunar Base :LunarBase: to {} will take {} and cost {} :Xe:, 25 :Water:, 75 :Ore:, "
                           "25 :Plasteel:, 25 :License:."
                           .format(coord, str(probe_time)
                                   , coord, str(pioneer_time), pioneer_xe, pioneer_w
                                   , coord, str(fs_time), fs_xe
                                   , coord, str(sos_time), sos_xe
                                   , coord, str(sv_time), sv_xe
                                   , coord, str(mo_time), mo_xe, mo_ore
                                   , coord, str(lb_time), lb_xe))
        elif mission == 'Probe' or mission == 'PB':
            await ctx.send("A Probe :Probe: to {} will take {} and cost 3 :Plasteel:".format(coord, str(probe_time)))
        elif mission == 'Pioneer' or mission == 'PN':
            await ctx.send("A Pioneer :Pioneer: to {} will take {} and cost {} :Xe:, {} :Water:, 2 :Plasteel:."
                           .format(coord, str(pioneer_time), pioneer_xe, pioneer_w))
        elif mission == 'Fuel Station' or mission == 'FS':
            await ctx.send("A Fuel Station :FuelStation: to {} will take {} and cost {} :Xe:, 3 :Water:, 3 :Ore:, "
                           "3 :Plasteel:.".format(coord, str(fs_time), fs_xe))
        elif mission == 'Small Orbital Station' or mission == 'SOS':
            await ctx.send("A Small Orbital Station :SmallOrbitalStation: to {} will take {} and cost {} :Xe:, "
                           "3 :Water:, 3 :Ore:, 1 :Plasteel:, 10 :License:.".format(coord, str(sos_time), sos_xe))
        elif mission == 'Science Vessel' or mission == 'SV':
            await ctx.send("A Science Vessel :ScienceVessel: to {} will take {} and cost {} :Xe:, 3 :Water:, "
                           "1 :Ore:, 10 :Plasteel:, 10 :License:.".format(coord, str(sv_time), sv_xe))
        elif mission == 'Mining Operation' or mission == 'MO':
            await ctx.send("A Mining Operation :MiningOperation: to {} will take {} and cost {} :Xe:, 5 :Water:, "
                           "{} :Ore:, 5 :Plasteel:, 5 :License:.".format(coord, str(mo_time), mo_xe, mo_ore))
        elif mission == 'Lunar Base' or mission == 'LB':
            await ctx.send("A Lunar Base :LunarBase: to {} will take {} and cost {} :Xe:, 25 :Water:, 75 :Ore:, "
                           "25 :Plasteel:, 25 :License:.".format(coord, str(lb_time), lb_xe))
        else:
            await ctx.send("`***ERROR*** You must enter a viable mission type, abbreviation, or 'All'.`")
        return

    # command info
    @commands.command(
        name='commission_e',
        description='Command to calculate commission for Probes, Pioneers, and Science Vessels to systems and planets, '
                    'given their rad-Z coordinates and any applicable upgrades.',
        aliases=['ce'],
        usage='<rad-Z> <# of stars+planets> <Mission (Probe/PB, Pioneer/PN, Science Vessel/SV)> '
              '<Astro-cartography Database upgrade (True/False)> <Printable Pocket Labs upgrade (True/False)> '
              '<Quantum Spectrometer upgrade (True/False)>'
    )
    @commands.dm_only()
    # function that command runs
    async def commission_e(self, ctx, coord, mission, explored=True, ad=True, ppl=False, qs=False, w_stars=0, o_stars=0,
                           rare_stars=0, other_stars=1, rare_planets=0, planets=0, planet_type="Uninhabitable"):
        if coord == '':  # checking for blank arg
            await ctx.send("`***ERROR:*** You need to list the system's/planet's coordinates.`")
        elif not re.search(r"\d{5}-\d{5}", coord):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the coordinates in the #####-##### format.`")
        elif not isinstance(w_stars, int) or not isinstance(o_stars, int) or not isinstance(rare_stars, int) \
                or not isinstance(other_stars, int) or not isinstance(rare_planets, int) \
                or not isinstance(planets, int):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the # of stars and planets as an integer`")
        else:  # if passes checks, parses args for calculation
            if explored:
                first = 1
            else:
                first = 2

            if mission == "Probe" or mission == "PB":
                if ad:
                    upgrade = 0.1 * (w_stars + o_stars + rare_stars + other_stars + rare_planets + planets)
                else:
                    upgrade = 0
                commission = (((w_stars * 10) + (o_stars * 2) + (rare_stars * 10) + (other_stars * 0.1) +
                               (rare_planets * 10) + (planets * 0.1)) + upgrade) * first
                await ctx.send("Sending a Probe :Probe: to {} will return a commission of {} :License:."
                               .format(coord, commission))
            elif mission == "Pioneer" or mission == "PN":
                p_types = {"Craters World": 1
                           , "Desert Craters World": 2
                           , "Desert Dunes World": 2
                           , "Desert Metal-rich World": 2
                           , "Desert Rocky World": 2
                           , "Desert Volcanic World": 2
                           , "Desert World": 1
                           , "Dunes Craters World": 2
                           , "Dunes Metal-rich World": 2
                           , "Dunes Rocky World": 2
                           , "Dunes Volcanic World": 2
                           , "Dunes World": 1
                           , "Metal-rich Craters World": 2
                           , "Metal-rich Volcanic World": 2
                           , "Metal-rich World": 1
                           , "Rocky Craters World": 2
                           , "Rocky Metal-rich World": 2
                           , "Rocky Volcanic World": 2
                           , "Rocky World": 1
                           , "Volcanic Craters World": 2
                           , "Volcanic World": 1
                           , "Rare Planetary Body": 10
                           , "Destroyed Planet": 0
                           , "Earth-like World": 0
                           , ":Water: World": 0
                           , "Moon": 0
                           , "Comet": 0
                           , "Uninhabitable": 0
                           }

                if ppl:
                    upgrade = 2
                else:
                    upgrade = 1
                commission = p_types[planet_type] * first * ppl
                await ctx.send("Sending Pioneers :Pioneer: to {} will return a commission of {} :License:."
                               .format(coord, commission))

            elif mission == "Science Vessel" or mission == "SV":
                if qs:
                    commission = 60
                else:
                    commission = 50
                await ctx.send("Sending a Science Vessel :ScienceVessel: to {} will return a commission of "
                               "{} :License:.".format(coord, commission))
            else:
                await ctx.send("`***ERROR*** You must enter a viable mission type or abbreviation.`")
        return

    # command info
    # noinspection PyUnboundLocalVariable
    @commands.command(
        name='mission_e',
        description='Command to calculate mission times to a system in "<days>, hh:mm:ss" format, '
                    'along with associated costs',
        aliases=['me2'],
        usage='<rad-Z 1> <rad-Z 2> <# of stars+planets> <Mission (All, Prob/PB, Pioneer/PN, Fuel Station/FS, '
              'Small Orbital Station/SOS, Science Vessel/SV, Mining Operation/MO, Lunar Base/LB)> '
              '<Subroutine Scanner upgrade (True/False)> <Augmented Workforce upgrade (True/False)> '
              'Subroutine Mining Drones upgrade (True/False)'
    )
    @commands.dm_only()
    # function that command runs
    async def mission2_e(self, ctx, coord1, coord2='00000-00000', bodies=1, mission="All", ss=False, aw=False, smd=False):
        # noinspection PyGlobalUndefined
        global probe_time
        if coord1 == '' or coord2 == '':  # checking for blank arg
            await ctx.send("`***ERROR:*** You need to list both systems' coordinates.`")
        elif not re.search(r"\d{5}-\d{5}", coord1) or not re.search(r"\d{5}-\d{5}", coord2):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the coordinates in the #####-##### format`")
        elif not isinstance(bodies, int):  # checking for arg format
            await ctx.send("`***ERROR:*** You must enter the # of stars and planets as an integer`")
        else:  # if passes checks, parses args for calculation
            r1 = int(re.search(r"^\d{5}", coord1).group(0))
            z1 = int(re.search(r"\d{5}$", coord1).group(0))
            r2 = int(re.search(r"^\d{5}", coord2).group(0))
            z2 = int(re.search(r"\d{5}$", coord2).group(0))
            dist = np.around(np.sqrt((np.square(z1) + np.square(z2)) -
                                     2 * (z1 * z2 * (np.cos((r1 - r2) / 10000)))) / 10, 1)
            dist_hours = np.floor(dist / 10)
            probe_time = dt.timedelta(hours=int(dist_hours + np.floor(bodies / 2)),
                                      minutes=int(((dist / 10) - dist_hours) * 60 + (bodies % 2) * 30))
            pioneer_time = dt.timedelta(hours=int(dist_hours + 6), minutes=int(((dist / 10) - dist_hours) * 60))
            pioneer_xe = np.ceil(dist / 10) * 0.1
            if ss:  # checks if player set upgrade value to T, may need to make this more robust
                pioneer_w = 2
            else:
                pioneer_w = 3
            fs_time = dt.timedelta(hours=int(dist_hours), minutes=int(((dist / 10) - dist_hours) * 60))
            fs_xe = np.around((np.ceil(dist / 10) * 0.2) + 1, 1)
            sos_time = dt.timedelta(hours=int(dist_hours + 6), minutes=int(((dist / 10) - dist_hours) * 60))
            sos_xe = np.around((np.ceil(dist / 10) * 0.3) + 3, 1)
            sv_time = fs_time + dt.timedelta(hours=72)
            sv_xe = np.around((np.ceil(dist / 10) * 0.2) + 1, 1)  # check if system is anomaly once connected to server
            if smd:
                mo_time = fs_time + dt.timedelta(hours=192)
            else:
                mo_time = fs_time + dt.timedelta(hours=168)
            mo_xe = np.around((np.ceil(dist / 10) * 0.3) + 1, 1)
            if aw:
                mo_ore = 0
            else:
                mo_ore = 5
            lb_time = fs_time + dt.timedelta(hours=168)
            lb_xe = np.around((np.ceil(dist / 10) * 1), 1)

        if mission == 'All':
            await ctx.send("A Probe :Probe: from {} to {} will take {} and cost 3 :Plasteel:\n"
                           "A Pioneer :Pioneer: from {} to {} will take {} and cost {} :Xe:, {} :Water:, "
                           "2 :Plasteel:.\n"
                           "A Fuel Station :FuelStation: from {} to {} will take {} and cost {} :Xe:, 3 :Water:, "
                           "3 :Ore:, 3 :Plasteel:.\n"
                           "A Small Orbital Station :SmallOrbitalStation: from {} to {} will take {} and cost {} :Xe:, "
                           "3 :Water:, 3 :Ore:, 1 :Plasteel:, 10 :License:.\n"
                           "A Science Vessel :Science Vessel: from {} to {} will take {} and cost {} :Xe:, 3 :Water:, "
                           "1 :Ore:, 10 :Plasteel:, 10 :License:.\n"
                           "A Mining Operation :MiningOperation: from {} to {} will take {} and cost {} :Xe:, "
                           "5 :Water:, {} :Ore:, 5 :Plasteel:, 5 :License:.\n"
                           "A Lunar Base :LunarBase: from {} to {} will take {} and cost {} :Xe:, 25 :Water:, "
                           "75 :Ore:, 25 :Plasteel:, 25 :License:."
                           .format(coord1, coord2, str(probe_time)
                                   , coord1, coord2, str(pioneer_time), pioneer_xe, pioneer_w
                                   , coord1, coord2, str(fs_time), fs_xe
                                   , coord1, coord2, str(sos_time), sos_xe
                                   , coord1, coord2, str(sv_time), sv_xe
                                   , coord1, coord2, str(mo_time), mo_xe, mo_ore
                                   , coord1, coord2, str(lb_time), lb_xe))
        elif mission == 'Probe' or mission == 'PB':
            await ctx.send("A Probe :Probe: from {} to {} will take {} and cost 3 :Plasteel:"
                           .format(coord1, coord2, str(probe_time)))
        elif mission == 'Pioneer' or mission == 'PN':
            await ctx.send("A Pioneer :Pioneer: from {} to {} will take {} and cost {} :Xe:, {} :Water:, "
                           "2 :Plasteel:.".format(coord1, coord2, str(pioneer_time), pioneer_xe, pioneer_w))
        elif mission == 'Fuel Station' or mission == 'FS':
            await ctx.send("A Fuel Station :FuelStation: from {} to {} will take {} and cost {} :Xe:, 3 :Water:, "
                           "3 :Ore:, 3 :Plasteel:.".format(coord1, coord2, str(fs_time), fs_xe))
        elif mission == 'Small Orbital Station' or mission == 'SOS':
            await ctx.send("A Small Orbital Station :SmallOrbitalStation: from {} to {} will take {} and cost "
                           "{} :Xe:, 3 :Water:, 3 :Ore:, 1 :Plasteel:, 10 :License:."
                           .format(coord1, coord2, str(sos_time), sos_xe))
        elif mission == 'Science Vessel' or mission == 'SV':
            await ctx.send("A Science Vessel :ScienceVessel: from {} to {} will take {} and cost {} :Xe:, "
                           "3 :Water:, 1 :Ore:, 10 :Plasteel:, 10 :License:."
                           .format(coord1, coord2, str(sv_time), sv_xe))
        elif mission == 'Mining Operation' or mission == 'MO':
            await ctx.send("A Mining Operation :MiningOperation: from {} to {} will take {} and cost {} :Xe:, "
                           "5 :Water:, {} :Ore:, 5 :Plasteel:, 5 :License:."
                           .format(coord1, coord2, str(mo_time), mo_xe, mo_ore))
        elif mission == 'Lunar Base' or mission == 'LB':
            await ctx.send(
                "A Lunar Base :LunarBase: from {} to {} will take {} and cost {} :Xe:, 25 :Water:, 75 :Ore:, "
                "25 :Plasteel:, 25 :License:.".format(coord1, coord2, str(lb_time), lb_xe))
        else:
            await ctx.send("`***ERROR*** You must enter a viable mission type, abbreviation, or 'All'.`")
        return


def setup(bot):
    bot.add_cog(Calculation2(bot))
