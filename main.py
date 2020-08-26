import json
import discord
from discord.ext import commands

# grabbing the config file
with open('config.json') as config_file:
    secrets = json.load(config_file)


# function to fetch the bot prefix
def get_prefix(bot_client, message):
    prefixes = [secrets['prefix']]
    return commands.when_mentioned_or(*prefixes)(bot_client, message)


client = discord.Client

# bot info
bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot to help Exogen players make calculations, and for mods/admins to manage the server.',
    case_insensitive=True
)

# gathering the commands
cogs = [
    'cogs.calcs'
    # , 'cogs.mod'
]


# command to add a user to a role
@bot.command(
    pass_context=True,
    name="assign",
    description="Bot assigns designated role to target member, or self if blank, where possible.\n"
                "This function is only available to moderators and up.",
    usage="<role> <member>"
)
@commands.has_permissions(manage_roles=True)
async def assign(ctx, role: discord.Role, member: discord.Member = None):
    member = member or ctx.message.author
    await member.add_roles(role)
    await ctx.send(str(member) + " was added to " + str(role) + ".")


@assign.error
async def assign_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(ctx.message.channel, text)


# command to remove a user to a role
@bot.command(
    pass_context=True,
    name="remove",
    description="Bot removes designated role to target member, or self if blank, where possible.\n"
                "This function is only available to moderators and up.",
    usage="<role> <member>"
)
@commands.has_permissions(manage_roles=True)
async def remove(ctx, role: discord.Role, member: discord.Member = None):
    member = member or ctx.message.author
    await member.remove_roles(role)
    await ctx.send(str(member) + " was removed from " + str(role) + ".")


@remove.error
async def remove_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(ctx.message.channel, text)


# limiting the eval command to just the bot owner
@bot.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, code):
    await ctx.send(eval(code))


@_eval.error
async def eval_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(ctx.message.channel, text)


# bot start up event
@bot.event
async def on_ready():
    print("The bot is ready!")
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print('------------------------------------------------------')
    await bot.change_presence(activity=discord.Game(name="Exogen"))
    # bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
    return

# run bot
bot.run(secrets['token'])
