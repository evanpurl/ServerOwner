import discord
from discord.ext import commands

loggingchannel = 1155640629473329273


class logginglisteners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:

            if loggingchannel:

                if message.channel.id == loggingchannel:
                    return
                channel = discord.utils.get(message.guild.channels, id=loggingchannel)
                if channel:
                    embed = discord.Embed(
                        title="Message Deleted", color=discord.Color.orange())
                    embed.add_field(name="Channel", value=message.channel.mention)
                    embed.add_field(name="Message", value=message.content[:1000])
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        try:

            if message_before.author.id == self.bot.user.id:
                return

            if loggingchannel:
                if message_before.channel.id == loggingchannel:
                    return
                channel = discord.utils.get(message_before.guild.channels, id=loggingchannel)
                if channel:
                    embed = discord.Embed(
                        title="Message Edited", color=discord.Color.orange())
                    embed.set_author(name=message_before.author.name, icon_url=message_before.author.avatar)
                    embed.add_field(name="Channel", value=message_before.channel.mention)
                    embed.add_field(name="Before", value=message_before.content[:1000])
                    embed.add_field(name="After", value=message_after.content[:1000])
                    embed.add_field(name="Link", value=message_after.jump_url)
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(channel.guild.channels, id=loggingchannel)
                if logchannel:
                    embed = discord.Embed(
                        title="Channel Created", color=discord.Color.orange())
                    embed.add_field(name="Channel", value=channel.mention)
                    embed.add_field(name="Name", value=channel.name)
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await logchannel.send(embed=embed)

        except Exception as e:
            print(f"Channel create: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.TextChannel):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(channel.guild.channels, id=loggingchannel)
                if logchannel:
                    embed = discord.Embed(
                        title="Channel Deleted", color=discord.Color.orange())
                    embed.add_field(name="Channel", value=channel.name)
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await logchannel.send(embed=embed)
        except Exception as e:
            print(f"Channel delete: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before: discord.TextChannel, channel_after: discord.TextChannel):
        try:
            if channel_before.name != channel_after.name:

                if loggingchannel:
                    logchannel = discord.utils.get(channel_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        embed = discord.Embed(
                            title="Channel Name Changed", color=discord.Color.orange())
                        embed.add_field(name="Before", value=channel_before.name)
                        embed.add_field(name="After", value=channel_after.name)
                        embed.set_thumbnail(url=self.bot.user.avatar)
                        await logchannel.send(embed=embed)
            if channel_before.topic != channel_after.topic:

                if loggingchannel:
                    logchannel = discord.utils.get(channel_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        embed = discord.Embed(
                            title="Channel Topic Changed", color=discord.Color.orange())
                        embed.add_field(name="Before", value=channel_before.topic)
                        embed.add_field(name="After", value=channel_after.topic)
                        embed.add_field(name="Channel Name", value=channel_after.name)
                        embed.add_field(name="Channel", value=channel_after.mention)
                        embed.set_thumbnail(url=self.bot.user.avatar)
                        await logchannel.send(embed=embed)
        except Exception as e:
            print(f"Role update: {e}")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(role.guild.channels, id=loggingchannel)
                if logchannel:
                    embed = discord.Embed(
                        title="Role Created", color=discord.Color.orange())
                    embed.add_field(name="Name", value=role.name)
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await logchannel.send(embed=embed)
        except Exception as e:
            print(f"Role create: {e}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(role.guild.channels, id=loggingchannel)
                if logchannel:
                    embed = discord.Embed(
                        title="Role Deleted", color=discord.Color.orange())
                    embed.add_field(name="Role", value=role.name)
                    embed.add_field(name="Name", value=role.name)
                    embed.set_thumbnail(url=self.bot.user.avatar)
                    await logchannel.send(embed=embed)
        except Exception as e:
            print(f"Role delete: {e}")

    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before: discord.Role, role_after: discord.Role):
        try:
            if role_before.name != role_after.name:

                if loggingchannel:
                    logchannel = discord.utils.get(role_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        embed = discord.Embed(
                            title="Role Name Changed", color=discord.Color.orange())
                        embed.add_field(name="Before", value=role_before.name)
                        embed.add_field(name="After", value=role_after.name)
                        embed.set_thumbnail(url=self.bot.user.avatar)
                        await logchannel.send(embed=embed)
        except Exception as e:
            print(f"Role update: {e}")


async def setup(bot: commands.Cog):
    await bot.add_cog(logginglisteners(bot))
