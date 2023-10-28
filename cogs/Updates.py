import datetime
import discord

from discord import app_commands, ui
from discord.ext import commands
from settings import *


class Updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = 1155534145443877095

    @app_commands.command(name="update", description="Send Updates!")
    @app_commands.choices(topic=[
        app_commands.Choice(name='General', value=1),
        app_commands.Choice(name='Discord', value=2),
        app_commands.Choice(name='Website', value=3),
        app_commands.Choice(name='Applications', value=4),
        app_commands.Choice(name='Other', value=5),
    ])
    async def update(self, interaction: discord.Interaction, topic: app_commands.Choice[int]):
        try:
            if interaction.user.guild_permissions.manage_channels:

                channel = discord.utils.get(interaction.guild.channels, id=self.channel)

                await interaction.response.send_modal(Updatemodal(self.client, channel, topic.name))
            else:
                await interaction.response.send_message(content=f"You do not have permission to run this command.",
                                                        ephemeral=True)

        except Exception as e:
            print(e)


async def assembleembed(server, choice, added, removed, updated):
    try:
        if added is None:
            added = "N/A"
        if removed is None:
            removed = "N/A"
        if updated is None:
            updated = "N/A"
        embed = discord.Embed(title=f"ServerOwner | New Updates!",
                              description=f"Here are the current updates for **{choice}**!",
                              color=discord.Color.orange(), timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name="Added", value=added, inline=False)
        embed.add_field(name="Removed", value=removed, inline=False)
        embed.add_field(name="Updated", value=updated, inline=False)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


class Updatemodal(ui.Modal, title='Update Information'):

    def __init__(self, bot, channel, topic):
        super().__init__()
        self.bot = bot
        self.channel = channel
        self.topic = topic

    added = ui.TextInput(label='Added:', style=discord.TextStyle.paragraph,
                         placeholder="N/A", required=False)
    removed = ui.TextInput(label='Removed:', style=discord.TextStyle.paragraph,
                           placeholder="N/A", required=False)
    updated = ui.TextInput(label='Updated:', style=discord.TextStyle.paragraph,
                           placeholder="N/A", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        if self.added.value == "":
            self.added = "N/A"
        if self.removed.value == "":
            self.removed = "N/A"
        if self.updated.value == "":
            self.updated = "N/A"

        await self.channel.send(
            embed=await assembleembed(interaction.guild, self.topic, self.added, self.removed, self.updated))

        await interaction.response.send_message(content=f"The update has been sent to the updates channel!",
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Updates(bot))
