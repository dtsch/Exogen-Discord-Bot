import discord
from discord.ext import commands



def get_prefix(bot_client, message):
    prefixes = ['!']
    return commands.when_mentioned_or(*prefixes)(bot_client, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot to help Exogen players make calculations',
    owner_id=725342626013904977,
    case_insensitive=True
)

cogs = ['cogs.basic', 'cogs.embed', 'cogs.calcs']



@bot.event
async def on_ready():
    print("The bot is ready!")
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print('---------------------------------------------')
    await bot.change_presence(activity=discord.Game(name="Exogen"))
    bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
    return

bot.run(TOKEN)
