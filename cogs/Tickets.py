import asyncio
import io
import chat_exporter
import discord
from discord import app_commands, ui
from discord.ext import commands
import datetime


def ticketmessageembed():
    embed = discord.Embed(title="**Tickets**",
                          description=f"Change me",
                          color=discord.Color.orange())
    embed.set_footer(text="©️ ServerOwner 2023")
    return embed


async def ticketembed(user, reason, server):
    embed = discord.Embed(title="ServerOwner | New Ticket!",
                          description=f"""Hello, {user.mention}. Thank you for reaching out to our Support Team! We'll be with you shortly. In the interim, please provide a detailed description of your concerns.""",
                          color=discord.Color.orange(), timestamp=datetime.datetime.now())
    embed.add_field(name=f"Reason:", value=reason, inline=True)
    embed.set_thumbnail(url=server.icon.url)
    embed.set_footer(text="©️ ServerOwner 2023")
    return embed


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="ticketbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"ticket-{interaction.user.name.lower()}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing ticket: {existticket.mention}.",
                    ephemeral=True)
            else:
                await interaction.response.send_modal(Ticketmodal(interaction.client))
        except Exception as e:
            print(e)


class Ticketmodal(ui.Modal, title='Ticket Creation'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    reason = ui.TextInput(label='Reason for Ticket:', style=discord.TextStyle.paragraph,
                          max_length=300)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
            ticketcat = discord.utils.get(interaction.guild.categories, id=1155718419665137665)
            if ticketcat:
                ticketchan = await interaction.guild.create_text_channel(
                    f"ticket-{interaction.user.name}", category=ticketcat,
                    overwrites=overwrites)

                await interaction.response.send_message(content=f"I've initiated a ticket within {ticketchan.mention}.",
                                                        ephemeral=True)
                await ticketchan.send(
                    content=f"{discord.utils.get(interaction.guild.roles, id=1156730288135753829).mention}",
                    embed=await ticketembed(interaction.user, self.reason, interaction.guild),
                    view=ticketbuttonpanel())

            else:  # If for some reason the ticket category can't be found, make the channel anyway.
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}

                ticketchan = await interaction.guild.create_text_channel(
                    f"ticket-{interaction.user.name}",
                    overwrites=overwrites)

                await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                        ephemeral=True)
                await ticketchan.send(
                    embed=await ticketembed(interaction.user, self.reason, interaction.guild),
                    view=ticketbuttonpanel())
        except Exception as e:
            print(e)


class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id=f"gsticket:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=1155617191828410418)
            if logchannel:
                transcriptdm = await chat_exporter.export(
                    interaction.channel,
                )
                transcripttochannel = await chat_exporter.export(
                    interaction.channel,
                )
                if transcriptdm is None:
                    return
                if transcripttochannel is None:
                    return

                transcript_file_to_dm = discord.File(
                    io.BytesIO(transcriptdm.encode()),
                    filename=f"transcript-{interaction.channel.name}.html",
                )
                transcript_file_to_channel = discord.File(
                    io.BytesIO(transcripttochannel.encode()),
                    filename=f"transcript-{interaction.channel.name}.html",
                )

                await interaction.user.send(file=transcript_file_to_dm)
                await logchannel.send(file=transcript_file_to_channel)

            await interaction.channel.delete()
        except Exception as e:
            print(e)


class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket", description="Command used to make a ticket.")
    async def ticket(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await channel.send(embed=ticketmessageembed(), view=ticketbutton())
            await interaction.response.send_message(content=f"Ticket message created in {channel.mention}", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="add", description="Includes a particular user in a ticket.")
    async def add(self, interaction: discord.Interaction, user: discord.Member) -> None:
        try:
            role = discord.utils.get(interaction.guild.roles, id=1156730288135753829)
            if role in interaction.user.roles:
                if interaction.channel.category.id == 1155718419665137665:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.read_messages = True
                    await interaction.channel.set_permissions(user, overwrite=overwrite)
                    await interaction.response.send_message(content=f"Added {user.name} to the ticket.",
                                                            ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"You are not currently within a ticket.", ephemeral=True)
            else:
                await interaction.response.send_message(content=f"Your access does not authorize the use of this command.", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="remove", description="Excludes a specific user from a ticket.")
    async def remove(self, interaction: discord.Interaction, user: discord.Member) -> None:
        try:
            role = discord.utils.get(interaction.guild.roles, id=1156730288135753829)
            if role in interaction.user.roles:
                if interaction.channel.category.id == 1155718419665137665:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    overwrite.read_messages = False
                    await interaction.channel.set_permissions(user, overwrite=overwrite)
                    await interaction.response.send_message(content=f"Removed {user.name} from the ticket.", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"You aren't in a ticket.", ephemeral=True)
            else:
                await interaction.response.send_message(content=f"Your access does not authorize the use of this command.", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="rename", description="Changes the name of the ongoing ticket.")
    async def rename(self, interaction: discord.Interaction, name: str) -> None:
        try:
            if interaction.channel.category.id == 1155718419665137665:
                role = discord.utils.get(interaction.guild.roles, id=1156730288135753829)
                if role in interaction.user.roles:
                    await interaction.channel.edit(name=name)
                    await interaction.response.send_message(content=f"The ticket has been renamed to {name}.",
                                                            ephemeral=True)

                else:
                    await interaction.response.send_message(content=f"You don't have permission to use this command.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(content=f"You aren't in a ticket.", ephemeral=True)
        except Exception as e:
            print(e)

    @ticket.error
    @add.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
    bot.add_view(ticketbuttonpanel())
    bot.add_view(ticketbutton())
