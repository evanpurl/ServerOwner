import discord
from discord.ext import commands
from utils.embeds import log_embed

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
                    await channel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Message Edit!", [["Channel:", message.channel.mention], ["Message:", message.content[:1000]]], self.bot))
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
                    await channel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Message Edit!", [["Channel:", channel.mention], ["Before:", message_before.content[:1000]], ["Before:", message_after.content[:1000]], ["Link:", message_after.jump_url]], self.bot))
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(channel.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Channel Creation!", [["Channel:", channel.mention], ["Name:", channel.name]], self.bot))

        except Exception as e:
            print(f"Channel create: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.TextChannel):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(channel.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Channel Deletion!", [["Channel:", channel.name]], self.bot))
                    return
        except Exception as e:
            print(f"Channel delete: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before: discord.TextChannel, channel_after: discord.TextChannel):
        try:
            if channel_before.name != channel_after.name:

                if loggingchannel:
                    logchannel = discord.utils.get(channel_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Channel Name Change!", [["Before:", channel_before.name], ["After:", channel_after.mention]], self.bot))
                        return
            if channel_before.topic != channel_after.topic:

                if loggingchannel:
                    logchannel = discord.utils.get(channel_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Channel Topic Change!", [["Before:", channel_before.topic], ["After:", channel_after.topic], ["Channel Name:", channel_after.name], ["Channel:", channel_after.mention]], self.bot))
                        return
        except Exception as e:
            print(f"Channel update: {e}")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(role.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Role Creation!", [["Name:", role.name]], self.bot))
                    return
        except Exception as e:
            print(f"Role create: {e}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        try:

            if loggingchannel:
                logchannel = discord.utils.get(role.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Role Deletion!", [["Role:", role.name], ["Name:", role.name]], self.bot))
                    return
        except Exception as e:
            print(f"Role delete: {e}")

    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before: discord.Role, role_after: discord.Role):
        try:
            if role_before.name != role_after.name:

                if loggingchannel:
                    logchannel = discord.utils.get(role_after.guild.channels, id=loggingchannel)
                    if logchannel:
                        await logchannel.send(embed=await log_embed(f"Description goes here", "ServerOwner | Role Change!", [["Before:", role_before.name], ["After:", role_after.name]], self.bot))
                        return
        except Exception as e:
            print(f"Role update: {e}")


async def setup(bot: commands.Cog):
    await bot.add_cog(logginglisteners(bot))
