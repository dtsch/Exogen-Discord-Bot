import discord
from discord.ext import commands

client = discord.Client()

ch = None
ro = None


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Sends the latency of the Bot', hidden=False)
    @commands.has_any_role('Assistant', 'Supervisor', 'Manager')
    async def ping(self, ctx):
        await ctx.send(f'**Pong!** Latency: {round(self.bot.latency * 1000)}ms')

    # command to add a user to a role
    @commands.command(
        pass_context=True,
        name="assign",
        description="Bot assigns designated role to target member, or self if blank, where possible.\n"
                    "This function is only available to moderators and up.",
        help='assigns server role',
        usage="<role> <member>"
    )
    @commands.has_permissions(manage_roles=True)
    # add Assistant, Supervisor, and Manager roles here
    async def assign(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.message.author
        await member.add_roles(role)
        await ctx.send(member.mention + " was added to " + role.mention + ".")

    @assign.error
    async def assign_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to remove a user to a role
    @commands.command(
        pass_context=True,
        name="remove",
        description="Bot removes designated role to target member, or self if blank, where possible.\n"
                    "This function is only available to moderators and up.",
        help='removes server role',
        usage="<role> <member>"
    )
    @commands.has_permissions(manage_roles=True)
    async def remove(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.message.author
        await member.remove_roles(role)
        await ctx.send(member.mention + " was removed from " + role.mention + ".")

    @remove.error
    async def remove_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to add a new channel
    @commands.command(
        pass_context=True,
        name="new_channel",
        description="Bot creates a new channel",
        help='adds new channel',
        aliases=['nc'],
        usage="<channel name>"
    )
    @commands.has_permissions(manage_channels=True)
    async def new_channel(self, ctx, name, cat: discord.CategoryChannel = None):
        channel = await discord.Guild.create_text_channel(ctx.guild, name, category=cat)
        await ctx.send("Congratulations! The new channel of " + channel.mention + " has been created")

    @new_channel.error
    async def new_channel_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to delete a channel
    @commands.command(
        pass_context=True,
        name="del_channel",
        description="Bot deletes a channel",
        help='deletes channel',
        aliases=['dc'],
        usage="<channel name>"
    )
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, name: discord.TextChannel):
        await name.delete()
        await ctx.send("Successfully deleted the " + name.mention + " channel.")

    @delete_channel.error
    async def delete_channel_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to create a new role
    @commands.command(
        pass_context=True,
        name="new_role",
        description="Bot creates a new role",
        help='creates new role',
        aliases=['nr'],
        usage="<role name>"
    )
    @commands.has_permissions(manage_roles=True)
    async def new_role(self, ctx, role_name):
        role = await ctx.guild.create_role(name=role_name)
        await ctx.send("Congratulations! The new role of " + role.mention + " has been created")

    @new_role.error
    async def new_role_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to delete a role
    @commands.command(
        pass_context=True,
        name="del_role",
        description="Bot deletes a role",
        help='deletes role',
        aliases=['dr'],
        usage="<channel name>"
    )
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, name: discord.Role):
        await name.delete()
        await ctx.send("Successfully deleted the " + name.mention + " role.")

    @delete_role.error
    async def delete_role_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command to create a role and private channel for a Mega Corp
    @commands.command(
        pass_context=True,
        name="create_mc",
        description="Bot creates a private channel and exclusive role for a new Mega Corp.\n"
                    "This function is only available to moderators and up.",
        help='creates new role and channel for a MC',
        aliases=['mc'],
        usage="<MC name> <MC handle>"
    )
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def create_mc(self, ctx, mc, handle, cat: discord.CategoryChannel = None):
        role = await ctx.guild.create_role(name=handle)
        overwrites = {
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await discord.Guild.create_text_channel(ctx.guild, handle, category=cat, overwrites=overwrites)
        await ctx.send("The Mega Corporation of **{}** has been instated, the private channel {} and role {} "
                       "have been created for it's members".format(mc, channel.mention, role.mention))

    @create_mc.error
    async def create_mc_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    # command that deletes role and private channel of a Mega Corp
    @commands.command(
        pass_context=True,
        name="delete_mc",
        description="Bot deletes a private channel and exclusive role for a new Mega Corp.\n"
                    "This function is only available to moderators and up.",
        help='deletes channel and role of MC',
        aliases=['dmc'],
        usage="<MC name> <MC handle>"
    )
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def delete_mc(self, ctx, channel: discord.TextChannel, role: discord.Role):
        global ch
        ch = channel
        global ro
        ro = role
        msg = await ctx.message.channel.send("Are you sure you wish to delete the role & channel for this Mega Corp?\n"
                                             "Please press {} or {} to confirm.".format(u"\u2705", u"\u274E"))
        await msg.add_reaction(u"\u2705")
        await msg.add_reaction(u"\u274E")

    @delete_mc.error
    async def delete_mc_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    ch = None
    ro = None

    # event that waits for users reaction to the previous message
    # noinspection PyUnresolvedReferences
    @client.event
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.emoji == u"\u2705":
            await ch.delete()
            await ro.delete()
            await reaction.message.channel.send("Successfully deleted the " + ch.mention + " channel and " +
                                                ro.mention + " role.")
            await reaction.message.delete()
            return
        elif reaction.emoji == u"\u274E":
            await reaction.message.delete()
            await reaction.message.channel.send("Mega Corp role and channel deletion aborted.")
            return
        else:
            return


def setup(bot):
    bot.add_cog(Moderation(bot))
