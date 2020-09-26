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
    await ctx.send(member.mention + " was added to " + role.mention + ".")


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
    await ctx.send(member.mention + " was removed from " + role.mention + ".")


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


@bot.command(
    pass_context=True,
    name="new_channel",
    description="Bot creates a new channel",
    aliases=['nc'],
    usage="<channel name>"
)
@commands.has_permissions(manage_channels=True)
async def new_channel(ctx, name, cat: discord.CategoryChannel = None):
    channel = await guild.create_text_channel(ctx.guild, name, category=cat)
    await ctx.send("Congratulations! The new channel of " + channel.mention + " has been created")


@bot.command(
    pass_context=True,
    name="del_channel",
    description="Bot deletes a channel",
    aliases=['dc'],
    usage="<channel name>"
)
@commands.has_permissions(manage_channels=True)
async def delete_channel(ctx, name: discord.TextChannel):
    await name.delete()
    await ctx.send("Successfully deleted the " + name.mention + " channel.")


@bot.command(
    pass_context=True,
    name="new_role",
    description="Bot creates a new role",
    aliases=['nr'],
    usage="<channel name>"
)
@commands.has_permissions(manage_roles=True)
async def new_role(ctx, role_name):
    role = await ctx.guild.create_role(name=role_name)
    await ctx.send("Congratulations! The new role of " + role.mention + " has been created")


@bot.command(
    pass_context=True,
    name="del_role",
    description="Bot deletes a role",
    aliases=['dr'],
    usage="<channel name>"
)
@commands.has_permissions(manage_roles=True)
async def delete_role(ctx, name: discord.Role):
    await name.delete()
    await ctx.send("Successfully deleted the " + name.mention + " role.")


@bot.command(
    pass_context=True,
    name="create_mc",
    description="Bot creates a private channel and exclusive role for a new Mega Corp.\n"
                "This function is only available to moderators and up.",
    aliases=['mc'],
    usage="<MC name> <MC handle>"
)
@commands.has_permissions(manage_channels=True, manage_roles=True)
async def create_mc(ctx, mc, handle, cat: discord.CategoryChannel = None):
    overwrites = {
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    role = await ctx.guild.create_role(name=handle)
    channel = await guild.create_text_channel(ctx.guild, handle, category=cat, overwrites=overwrites)
    await ctx.send("The Mega Corporation of **{}** has been instated, the private channel {} and role {} "
                   "have been created for it's members".format(mc, channel.mention, role.mention))


ch = None
ro = None


@bot.command(
    pass_context=True,
    name="delete_mc",
    description="Bot deletes a private channel and exclusive role for a new Mega Corp.\n"
                "This function is only available to moderators and up.",
    aliases=['dmc'],
    usage="<MC name> <MC handle>"
)
@commands.has_permissions(manage_channels=True, manage_roles=True)
async def delete_mc(ctx, channel: discord.TextChannel, role: discord.Role):
    global ch
    ch = channel
    global ro
    ro = role
    msg = await ctx.message.channel.send("Are you sure you wish to delete the role and channel for this Mega Corp?\n"
                                         "Please press {} or {}.".format(u"\u2705", u"\u274E"))
    await msg.add_reaction(u"\u2705")
    await msg.add_reaction(u"\u274E")


# noinspection PyUnresolvedReferences
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.emoji == u"\u2705":
        await ch.delete()
        await ro.delete()
        await reaction.message.channel.send("Successfully deleted the " + ch.mention + " channel and " +
                                            ro.mention + " role.")
        await reaction.message.clear_reactions()
        return
    elif reaction.emoji == u"\u274E":
        await reaction.message.delete()
        await reaction.message.channel.send("Mega Corp role and channel deletion aborted.")
        return
    else:
        return


@delete_mc.error
async def delete_mc_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        txt = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(ctx.message.channel, txt)


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
