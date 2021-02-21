import asyncio
import requests
import json
import re
import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import keep_alive


# # grabbing the config file
# with open('config.json') as config_file:
#     secrets = json.load(config_file)

# grabbing keys
token = os.getenv("bot_token")
key = os.getenv("api_key")


# intents so bot can see members from DMs
intents = discord.Intents(messages=True, reactions=True, members=True, guilds=True, presences=True)


# bot info
bot = commands.Bot(
    command_prefix='!'
    , description='Bot to help Exogen players make calculations, and for mods/admins to manage the server.'
    , case_insensitive=True
    , intents=intents
)
# background task to keep bot awake when web-hosted on Repl.it
status = cycle(['Exogen  ░░░░░░░░',
                'Exogen  ░░░░░░░▒',
                'Exogen  ░░░░░░▒▓',
                'Exogen  ░░░░░▒▓▒',
                'Exogen  ░░░░▒▓▒░',
                'Exogen  ░░░▒▓▒░░',
                'Exogen  ░░▒▓▒░░░',
                'Exogen  ░▒▓▒░░░░',
                'Exogen  ▒▓▒░░░░░',
                'Exogen  ▓▒░░░░░░',
                'Exogen  ▒░░░░░░░',
                'Exogen  ░░░░░░░░',
                'Exogen  ▒░░░░░░░',
                'Exogen  ▓▒░░░░░░',
                'Exogen  ▒▓▒░░░░░',
                'Exogen  ░▒▓▒░░░░',
                'Exogen  ░░▒▓▒░░░',
                'Exogen  ░░░▒▓▒░░',
                'Exogen  ░░░░▒▓▒░',
                'Exogen  ░░░░░▒▓▒',
                'Exogen  ░░░░░░▒▓',
                'Exogen  ░░░░░░░▒'])


# @bot.event
# async def on_ready():
#     change_status.start()
#     print("Your bot is ready")


@tasks.loop(seconds=2)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# gathering the commands
cogs = [
    'cogs.mod'
    , 'cogs.advisors'
    , 'cogs.calcs'
]


# limiting the eval command to just the bot owner
@bot.command(name='eval', hidden=True)
@commands.is_owner()
async def _eval(ctx, *, code):
    await ctx.send(eval(code))


@_eval.error
async def eval_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(ctx.message.channel, text)


# command that DMs the sender
@bot.command(
    pass_context=True,
    name='direct_message',
    description='Initiates a DM with the user.',
    help='starts a DM with the user',
    aliases=['dm'],
    usage=''
)
async def dm(ctx):
    await ctx.author.send("Hey, what do you need?")


@bot.event
async def on_member_join(member):
    rules = bot.get_channel(704733802223894648)
    nav = bot.get_channel(771885969715626005)
    await member.send("Welcome, {}!".format(member.name))
    await member.send("Please check out the {} before heading over to {} to see where things are located."
                      .format(rules.mention, nav.mention))
    await member.send("If you are unfamiliar with Exogen, feel free to check out the manual:\n"
                      "https://discordapp.com/channels/637447316856373268/704724317279092756/705170179893624943\n"
                      "And for advice on getting your corporation up and running, check out this startup guide from "
                      "the Pale Blue Dot megacorp:\n"
                      "https://discord.com/channels/637447316856373268/704733458227789937/745698128627236965")


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = discord.utils.get(guild.members, id=payload.user_id)
    # rules reaction role
    if payload.channel_id == 704733802223894648 and payload.message_id == 706999325556867163:
        role = discord.utils.get(payload.member.guild.roles, name="Accepted Rules")
        if str(payload.emoji) == '<:Exogen:749051544745541744>': # or str(payload.emoji) == '👍':
            await payload.member.add_roles(role)
    # RP reaction role
    elif payload.channel_id == 774834872719507496 and payload.message_id == 774845668745019392:
        role = discord.utils.get(payload.member.guild.roles, name="RP opt in")
        if str(payload.emoji) == '<:BHC:749478461562683443>':
            await payload.member.add_roles(role)
    # wiki reaction role
    elif payload.channel_id == 794598980973363210 and payload.message_id == 794600306532548618:
        role = discord.utils.get(payload.member.guild.roles, name="Researcher")
        if str(payload.emoji) == '<:ArchangelFoundation:749053627947286548>':
            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = discord.utils.get(guild.members, id=payload.user_id)
    # rules reaction role
    if payload.channel_id == 704733802223894648 and payload.message_id == 706999325556867163:
        role = discord.utils.get(guild.roles, name="Accepted Rules")
        if str(payload.emoji) == '<:Exogen:749051544745541744>':  # or str(payload.emoji) == '👍':
            await member.remove_roles(role)
    # RP reaction role
    elif payload.channel_id == 774834872719507496 and payload.message_id == 774845668745019392:
        role = discord.utils.get(guild.roles, name="RP opt in")
        if str(payload.emoji) == '<:BHC:749478461562683443>':
            await member.remove_roles(role)
    # wiki reaction role
    elif payload.channel_id == 794598980973363210 and payload.message_id == 794600306532548618:
        role = discord.utils.get(guild.roles, name="Researcher")
        if str(payload.emoji) == '<:ArchangelFoundation:749053627947286548>':
            await member.remove_roles(role)


# bot start up event
@bot.event
async def on_ready():
    print("The bot is ready!")
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print(f'Discord version is: {discord.__version__}')
    print('------------------------------------------------------')
    await bot.change_presence(activity=discord.Game(name="Exogen"))
    change_status.start()
    for cog in cogs:
        bot.load_extension(cog)
        print(f'{cog} is ready.')
    print('------------------------------------------------------')
    return

# run Flask script to keep bot online
keep_alive.keep_alive()

# run bot
# bot.run(secrets['token'])
bot.run(token)
