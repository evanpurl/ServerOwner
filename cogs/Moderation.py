import discord
from discord import app_commands
from discord.ext import commands
from sqlite3 import Error
from utils.sqlite import create_db, get_warnings, insert_warning, remove_warnings
from utils.embeds import user_warning_embed, user_warned_embed, log_embed

loggingchannel = 1155640629473329273


class moderationcmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Moderation command to warn a server member")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        try:
            #  Disable / enable goes here
            db = await create_db(f"storage/{interaction.guild.id}/moderation.db")
            await insert_warning(db, [user.id, reason])
            await interaction.response.send_message(
                content=f"User {user.mention} has been warned for reason **{reason}**.", ephemeral=True)
            #  Logging feature

            if loggingchannel:
                logchannel = discord.utils.get(interaction.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(
                        embed=await log_embed("Warning Created", [["User", user.name], ["Reason", reason]], self.bot))
                    #
            num_reasons = await get_warnings(db, user.id)
            if num_reasons:
                await user.send(embed=await user_warned_embed(user, reason, len(num_reasons)))
            else:
                await user.send(embed=await user_warned_embed(user, reason, 1))

        except Exception as e:
            print(e)

    @app_commands.command(name="get-warnings", description="Moderation command to get warnings from a server member")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def get_warnings(self, interaction: discord.Interaction, user: discord.Member, private_msg: bool):
        try:
            db = await create_db(f"storage/{interaction.guild.id}/moderation.db")
            warnings = await get_warnings(db, user.id)
            if warnings:
                await interaction.response.send_message(embed=await user_warning_embed(user, warnings),
                                                        ephemeral=private_msg)
            else:
                await interaction.response.send_message(content=f"""User {user.mention} has no warnings!""")

        except Exception or Error as e:
            print(e)

    @app_commands.command(name="clear-warnings", description="Moderation command to clear warnings for a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_warnings(self, interaction: discord.Interaction, user: discord.Member, private_msg: bool):
        try:
            db = await create_db(f"storage/{interaction.guild.id}/moderation.db")
            await remove_warnings(db, user.id)
            #  Logging feature

            if loggingchannel:
                logchannel = discord.utils.get(interaction.guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(
                        embed=await log_embed("Warnings Cleared", [["User", user.name]], self.bot))
                    #
            await interaction.response.send_message(content=f"Warnings for user {user.mention} have been cleared.",
                                                    ephemeral=private_msg)

        except Exception or Error as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            db = await create_db(f"storage/{guild.id}/moderation.db")
            await remove_warnings(db, user.id)

            #  Logging feature
            if loggingchannel:
                logchannel = discord.utils.get(guild.channels, id=loggingchannel)
                if logchannel:
                    await logchannel.send(embed=await log_embed("User Banned", [["User", user.name]], self.bot))
                    #

        except Exception as e:
            print(f"On Ready: {e}")


async def setup(bot):
    await bot.add_cog(moderationcmds(bot))
