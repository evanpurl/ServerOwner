import asyncio
import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands

verifiedchannel = 1160657156119478352
unverifiedchannel = 1160657284167385239

verifiedroles = [1155530172997566511, 1159314544347324466, 1159314541381959710]  # Reputable 1, 2, 3


async def reportembed(server, user, origuser, detailedreport, evidence):
    try:

        embed = discord.Embed(title=f"ServerOwner | New Report!",
                              description=f"""A new report has been created by {origuser.mention}.""",
                              color=discord.Color.orange())
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name=f"Discord Username:", value=user.mention, inline=False)
        embed.add_field(name=f"Detailed Report:", value=detailedreport, inline=False)
        embed.add_field(name=f"Evidence:", value=evidence, inline=False)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


class Reportmodal(ui.Modal, title='New Report'):

    def __init__(self, user):
        super().__init__()
        self.user = user

    detailedreport = ui.TextInput(label='Detailed Report:', style=discord.TextStyle.paragraph,
                                  max_length=1024)
    evidence = ui.TextInput(label='Evidence:', style=discord.TextStyle.paragraph,
                                  max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        if any(role.id in verifiedroles for role in interaction.user.roles):  # looks for role id in user's roles.
            channel = discord.utils.get(interaction.guild.channels, id=verifiedchannel)
            await channel.send(embed=await reportembed(interaction.guild, self.user, interaction.user, self.detailedreport, self.evidence))
            await interaction.response.send_message(content=f"Your report has been posted in {channel.mention}", ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, id=unverifiedchannel)
            await channel.send(embed=await reportembed(interaction.guild, self.user, interaction.user, self.detailedreport, self.evidence))
            await interaction.response.send_message(content=f"Your report has been posted in {channel.mention}", ephemeral=True)


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Command used to create a report.")
    async def report(self, interaction: discord.Interaction, user: discord.Member) -> None:
        try:
            if interaction.user.id == user.id:
                await interaction.response.send_message(content=f"You can't report yourself.", ephemeral=True)
            else:
                await interaction.response.send_modal(Reportmodal(user))
        except Exception as e:
            print(e)

    @report.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Report(bot))
