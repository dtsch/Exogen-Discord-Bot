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
        description='Command to measure distance between two systems, given their rad-Z coordinates.\n'
                    'Second coordinate is set to Sol (00000-00000) by default.',
        aliases=['d'],
        usage='<rad-Z 1> <rad-Z 2>\n'
              'ex: !d 44053-00043 00000-00000'
    )
    @commands.dm_only()
    # function that command runs
    async def distance(self, ctx, destination, origin='Sol'):
        if destination == 'Sol' or destination == 'sol':
            destination = '00000-00000'
        elif origin == 'Sol' or origin == 'sol':
            origin = '00000-00000'

        if destination == '':  # checking for blank arg
            await ctx.author.send("`***ERROR:*** You need to list the first system's coordinates.`")
        elif origin == '':  # checking for blank arg
            await ctx.author.send("`***ERROR:*** You need to list the second system's coordinates.`")
        elif not re.search(r"\d{5}-\d{5}", destination):  # checking for arg format
            await ctx.author.send("`***ERROR:*** You must enter the coordinates in the #####-##### format.`")
        elif not re.search(r"\d{5}-\d{5}", origin):  # checking for arg format
            await ctx.author.send("`***ERROR:*** You must enter the coordinates in the #####-##### format.`")
        else:  # if passes checks, parses args for calculation
            r1 = int(re.search(r"^\d{5}", destination).group(0))
            z1 = int(re.search(r"\d{5}$", destination).group(0))
            r2 = int(re.search(r"^\d{5}", origin).group(0))
            z2 = int(re.search(r"\d{5}$", origin).group(0))
            dist = np.around(np.sqrt((np.square(z1) + np.square(z2)) -
                                     2 * (z1 * z2 * (np.cos((r1 - r2) / 10000)))) / 10, 1)
            if destination == '00000-00000':
                destination = 'Sol'
            elif origin == '00000-00000':
                origin = 'Sol'
            await ctx.author.send("`The distance between {} and {} is {}JU.`".format(destination, origin, dist))
        return

    # calculates commission of various missions
    @commands.command(
        name='commission',
        description='Command to calculate commission for Probes, Pioneers, and Science Vessels to systems and planets, '
                    'given their rad-Z coordinates and any applicable upgrades.\n'
                    'Origin coordinate is set to Sol (00000-00000) by default.',
        aliases=['c'],
        usage='<destination rad-Z> <origin rad-Z> '
              '<Mission (Probe/PB, Pioneer/PN, Science Vessel/SV)> <Previously explored (True/False)> '
              '<Astro-cartography Database upgrade (True/False)> '
              '<Printable Pocket Labs upgrade (True/False)> <Quantum Spectrometer upgrade (True/False)> <w_stars> '
              '<o_stars> <rare_stars> <other_stars> <rare_planets> <other_planets> '
              '<planet_type (Craters/Desert/Dunes/Metal-rich/Rocky/Volcanic/Earth-like World) or combinations of two '
              'types, using capitalization and spaces>\n'
              'ex: !c 44053-00043 00000-00000 PB True True True True 0 0 0 3 0 5\n'
              'ex: !c 44053-00043 00000-00000 PN True True True True 0 0 0 3 0 5 "Desert Dunes World"\n'
    )
    @commands.dm_only()
    # function that command runs
    async def commission(self, ctx, destination, origin='Sol', mission='', explored=True, ad=True, ppl=False,
                         qs=False, w_stars=0, o_stars=0, rare_stars=0, other_stars=1, rare_planets=0, other_planets=0,
                         planet_type='Uninhabitable'):
        if destination == '':  # checking for blank arg
            await ctx.author.send("`***ERROR:*** You need to list the system's/planet's coordinates.`")
        elif not re.search(r"\d{5}-\d{5}", destination):  # checking for arg format
            await ctx.author.send("`***ERROR:*** You must enter the coordinates in the #####-##### format.`")
        elif not isinstance(w_stars, int) or not isinstance(o_stars, int) or not isinstance(rare_stars, int) \
                or not isinstance(other_stars, int) or not isinstance(rare_planets, int) \
                or not isinstance(other_planets, int):  # checking for arg format
            await ctx.author.send("`***ERROR:*** You must enter the # of stars and planets as an integer`")
        elif mission == '':
            await ctx.author.send("`***ERROR:*** You must enter a mission type.`")
        else:  # if passes checks, parses args for calculation
            if destination == 'Sol' or destination == 'sol':
                destination = '00000-00000'
            elif origin == 'Sol' or origin == 'sol':
                origin = '00000-00000'

            if explored:
                first = 1
            else:
                first = 2

            if mission == "Probe" or mission == "PB":
                if ad:
                    upgrade = 0.1 * (w_stars + o_stars + rare_stars + other_stars + rare_planets + other_planets)
                else:
                    upgrade = 0
                commission = (((w_stars * 10) + (o_stars * 2) + (rare_stars * 10) + (other_stars * 0.1) +
                               (rare_planets * 10) + (other_planets * 0.1)) + upgrade) * first
                await ctx.author.send("```Sending a Probe to {} will return a commission of {} Licenses.```"
                                      .format(destination, commission))
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
                           , "Earth-like World": 10
                           , "Water World": 0
                           , "Moon": 0
                           , "Comet": 0
                           , "Uninhabitable": 0
                           }
                if planet_type in p_types:
                    if ppl:
                        upgrade = 2
                    else:
                        upgrade = 1
                    commission = p_types[planet_type] * first * ppl * upgrade
                    await ctx.author.send("```Sending Pioneers to {} will return a commission of {} Licenses.```"
                                          .format(destination, commission))
                else:
                    await ctx.author.send("`***ERROR:*** You must enter a valid planet type.`")
            elif mission == "Science Vessel" or mission == "SV":
                if qs:
                    commission = 60
                else:
                    commission = 50
                await ctx.author.send("```Sending a Science Vessel to {} will return a commission of {} Licenses.```"
                                      .format(destination, commission))
            else:
                await ctx.author.send("```***ERROR*** You must enter a viable mission type or abbreviation.```")
        return

    # command info
    # noinspection PyUnboundLocalVariable
    @commands.command(
        name='missions',
        description='Command to calculate mission times to a system in "<days>, hh:mm:ss" format, '
                    'along with associated costs.\n'
                    'Origin coordinate is set to Sol (00000-00000) by default.',
        aliases=['m'],
        usage='<destination rad-Z> <origin rad-Z> <# of bodies> '
              '<Mission (All, Probe/PB, Pioneer/PN, Fuel Station/FS, Small Orbital Station/SOS, '
              'Science Vessel/SV, Mining Operation/MO, Lunar Base/LB)> '
              '<Subroutine Scanner upgrade (True/False)> <Augmented Workforce upgrade (True/False)> '
              '<Subroutine Mining Drones upgrade (True/False)> <Vapor Laser Extractors (True/False)>'
              '<Mining type (Exo/Moon/Ring/Exo & Ring/Comet)>\n'
              'ex: !m 44053-00043 00000-00000 5 All True True False False Exo'
    )
    @commands.dm_only()
    # function that command runs
    async def mission(self, ctx, destination, origin='Sol', bodies=1, mission="All", ss=False, aw=False, smd=False,
                      vle=False, mo_type='N/A'):
        # noinspection PyGlobalUndefined
        global probe_time
        if destination == 'Sol' or destination == 'sol':
            destination = '00000-00000'
        elif origin == 'Sol' or origin == 'sol':
            origin = '00000-00000'

        if destination == '' or origin == '':  # checking for blank arg
            await ctx.author.send("`***ERROR:*** You need to list both systems' coordinates.`")
        elif not re.search(r"\d{5}-\d{5}", destination) or not re.search(r"\d{5}-\d{5}", origin):  # checking arg format
            await ctx.author.send("`***ERROR:*** You must enter the coordinates in the #####-##### format`")
        elif not isinstance(bodies, int):  # checking for arg format
            await ctx.author.send("`***ERROR:*** You must enter the # of stars and planets as an integer`")
        else:  # if passes checks, parses args for calculation
            smd_types = ['Ring', 'Exo & Ring']
            r1 = int(re.search(r"^\d{5}", destination).group(0))
            z1 = int(re.search(r"\d{5}$", destination).group(0))
            r2 = int(re.search(r"^\d{5}", origin).group(0))
            z2 = int(re.search(r"\d{5}$", origin).group(0))
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
            smd_types = ['Ring', 'Exo & Ring']
            if smd and mo_type in smd_types:
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

        if destination == '00000-00000':
            destination = 'Sol'
        elif origin == '00000-00000':
            origin = 'Sol'
        probe = f'```A Probe from {origin} to {destination} will take {str(probe_time)} and cost 3 Plasteel.```\n'
        pioneer = f'```A Pioneer from {origin} to {destination} will take {str(pioneer_time)} and cost ' \
                  f'{pioneer_xe} Xe, {pioneer_w} Water, 2 Plasteel.```\n'
        fs = f'```A Fuel Station from {origin} to {destination} will take {str(fs_time)} and cost {fs_xe} Xe, ' \
             f'3 Water, 3 Ore, 3 Plasteel.```\n'
        sos = f'```A Small Orbital Station from {origin} to {destination} will take {str(sos_time)} and cost ' \
              f'{sos_xe} Xe, 3 Water, 3 Ore, 1 Plasteel, 10 Licenses.```\n'
        sv = f'```A Science Vessel from {origin} to {destination} will take {str(sv_time)} and cost {sv_xe} Xe, ' \
             f'3 Water, 1 Ore, 10 Plasteel, 10 Licenses.```\n'
        mo = f'```A Mining Operation from {origin} to {destination} will take {str(mo_time)} and cost {mo_xe} Xe, ' \
             f'5 Water, {mo_ore} Ore, 5 Plasteel, 5 Licenses.```\n'
        lb = f'```A Lunar Base from {origin} to {destination} will take {str(lb_time)} and cost {lb_xe} Xe, ' \
             f'25 Water, 75 Ore, 25 Plasteel, 25 Licenses.```\n'

        if mission == 'All':
            await ctx.author.send(probe + pioneer + fs + sos + sv + mo + lb)
        elif mission == 'Probe' or mission == 'PB':
            await ctx.author.send(probe)
        elif mission == 'Pioneer' or mission == 'PN':
            await ctx.author.send(pioneer)
        elif mission == 'Fuel Station' or mission == 'FS':
            await ctx.author.send(fs)
        elif mission == 'Small Orbital Station' or mission == 'SOS':
            await ctx.author.send(sos)
        elif mission == 'Science Vessel' or mission == 'SV':
            await ctx.author.send(sv)
        elif mission == 'Mining Operation' or mission == 'MO':
            await ctx.author.send(mo)
        elif mission == 'Lunar Base' or mission == 'LB':
            await ctx.author.send(lb)
        else:
            await ctx.author.send("```***ERROR*** You must enter a viable mission type, abbreviation, or 'All'.```")
        return


def setup(bot):
    bot.add_cog(Calculation(bot))
