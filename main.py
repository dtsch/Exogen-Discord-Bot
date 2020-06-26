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


# bot info
bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot to help Exogen players make calculations',
    owner_id=secrets['owner_id'],
    case_insensitive=True
)

# gathering the commands
cogs = ['cogs.calcs']


# limiting the eval command to just the bot owner
@bot.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, code):
    await ctx.send(eval(code))


# bot start up event
@bot.event
async def on_ready():
    print("The bot is ready!")
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print('---------------------------------------------')
    await bot.change_presence(activity=discord.Game(name="Exogen"))
    # bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
    return

# run bot
bot.run(secrets['token'])
