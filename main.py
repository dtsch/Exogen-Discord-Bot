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
guild = discord.Guild

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
]


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

#
# ch = None
# ro = None
#
#
# # command that deletes role and private channel of a Mega Corp
# @bot.command(
#     pass_context=True,
#     name="delete_mc",
#     description="Bot deletes a private channel and exclusive role for a new Mega Corp.\n"
#                 "This function is only available to moderators and up.",
#     aliases=['dmc'],
#     usage="<MC name> <MC handle>"
# )
# @commands.has_permissions(manage_channels=True, manage_roles=True)
# async def delete_mc(ctx, channel: discord.TextChannel, role: discord.Role):
#     global ch
#     ch = channel
#     global ro
#     ro = role
#     msg = await ctx.message.channel.send("Are you sure you wish to delete the role and channel for this Mega Corp?\n"
#                                          "Please press {} or {} to confirm.".format(u"\u2705", u"\u274E"))
#     await msg.add_reaction(u"\u2705")
#     await msg.add_reaction(u"\u274E")
#
#
# @delete_mc.error
# async def delete_mc_error(error, ctx):
#     if isinstance(error, commands.MissingPermissions):
#         text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
#         await ctx.send(ctx.message.channel, text)


# # event that waits for users reaction to the previous message
# # noinspection PyUnresolvedReferences
# @bot.event
# async def on_reaction_add(reaction, user):
#     if user.bot:
#         return
#
#     if reaction.emoji == u"\u2705":
#         await ch.delete()
#         await ro.delete()
#         await reaction.message.channel.send("Successfully deleted the " + ch.mention + " channel and " +
#                                             ro.mention + " role.")
#         await reaction.message.delete()
#         return
#     elif reaction.emoji == u"\u274E":
#         await reaction.message.delete()
#         await reaction.message.channel.send("Mega Corp role and channel deletion aborted.")
#         return
#     else:
#         return


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
