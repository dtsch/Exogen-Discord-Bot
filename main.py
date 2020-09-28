import asyncio
import json
import re
import discord
from discord.ext import commands

# grabbing the config file
with open('config.json') as config_file:
    secrets = json.load(config_file)


# function to fetch the bot prefix
def get_prefix(bot_client, message):
    prefixes = [secrets['prefix']]
    return commands.when_mentioned_or(*prefixes)(bot_client, message)


# bot info
bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot to help Exogen players make calculations, and for mods/admins to manage the server.',
    case_insensitive=True
)

# gathering the commands
cogs = [
    'cogs.calcs'
    , 'cogs.calcs2'
    , 'cogs.mod'
    , 'cogs.advisors'
]

database = ['D8GM3S', 'token6']
target_server_id = 704139386501201942
target_channel_id = 725386567740555416
target_role_id = 760186396555739197


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
    aliases=['dm', 'priv'],
    usage=''
)
async def dm(ctx):
    await ctx.author.send("Hey, what do you need?")


# command to add a user to a role
@bot.command(
    pass_context=True,
    name='token',
    description='Bot replies to sender in DM to verify registration as a donor in order to grant Advisor status.\n'
                'Can only be used in DMs.',
    usage='<token>',
    aliases=['advisor'],
    hidden=True
)
async def advisor_token(ctx, token: str = None):
    if ctx.message.guild is not None:
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send("This command can only be used in a DM channel.\n Try `!dm` to start a DM with me.")
    elif token is None:  # returning info about verifying donor status
        await asyncio.sleep(1)
        await ctx.author.send("**ERROR:** Please enter a token.")
    elif not re.search(r"[a-zA-Z0-9]{6}", token):  # checking for token for format
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.author.send("**ERROR:** You need to enter a token in the correct format.")
    elif token not in database:  # checking if token not in database
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.author.send("**ERROR:** I'm sorry, but I cannot find this token in our database. "
                                  "Please try again in a few minutes (donation can be still processed) "
                                  "or contact us directly.")
    elif token in database:  # checking if token exists in database
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.author.send("Checking database.")
        async with ctx.typing():
            await asyncio.sleep(2)
            await ctx.author.send("Your token has been found.\nActivating donor rewards.")

        # do stuff to check for token and add Advisor role in Exogen Discord server
        guild = bot.get_guild(target_server_id)
        channel = bot.get_channel(target_channel_id)
        role = guild.get_role(target_role_id)
        role_name = '@' + role.name
        member = guild.get_member(ctx.message.author.id)
        if member:
            await member.add_roles(role)

        async with ctx.typing():
            await asyncio.sleep(2)
            await ctx.author.send("Congratulations {} and welcome to the {}'s channel {}!"
                                  .format(member.mention, role_name, channel.mention))


# bot start up event
@bot.event
async def on_ready():
    print("The bot is ready!")
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print(f'Discord version is: {discord.__version__}')
    print('------------------------------------------------------')
    await bot.change_presence(activity=discord.Game(name="Exogen"))
    # bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
    return


# run bot
bot.run(secrets['token'])
