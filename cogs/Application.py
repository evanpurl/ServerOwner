import asyncio
import io
import chat_exporter
import discord
from discord import app_commands, ui
from discord.ext import commands


def applicationmessageembed(server):
    embed = discord.Embed(title=f"ServerOwner | Support Agent Applications",
                          description=f"ServerOwner, your ultimate Discord Hub for Minecraft server enthusiasts, is delighted to have you join our support team. Whether you're new to the community, a dedicated agent, a talented person, or a unique person, you've found your new home for being an agent. We offer a variety of things tailored to your expertise and interests.\n\n**We are looking for the following:**\n- Support Operatives\n- Support Agents\n\nFeel as if any of these positions are right for you? Click below to make your application! Make sure to fill it out with tons of enthusiastic details that will help you within the process.",
                          color=discord.Color.orange())
    embed.set_thumbnail(url=server.icon.url)
    embed.set_footer(text=f"© ServerOwner 2023")
    return embed


async def applicationembed(server, user, nametz, applyfor, portfolioresume, aboutinfo, whyapply):
    try:

        embed = discord.Embed(title=f"ServerOwner | New Application!",
                              description=f"""A new application has been submitted by {user.mention}.""",
                              color=discord.Color.orange())
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name=f"Name and Timezone:", value=nametz, inline=False)
        embed.add_field(name=f"What are you applying for:", value=applyfor, inline=False)
        embed.add_field(name=f"Portfolio and Resume:", value=portfolioresume, inline=False)
        embed.add_field(name=f"Tell us a bit about yourself:", value=aboutinfo, inline=False)
        embed.add_field(name=f"Why are you applying at ServerOwner?:", value=whyapply, inline=False)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


class Applicationmodal(ui.Modal, title='Support Agent Application'):
    nametz = ui.TextInput(label='Name and Timezone:', style=discord.TextStyle.short, max_length=100)
    applyfor = ui.TextInput(label='What are you applying for:', style=discord.TextStyle.paragraph,
                            max_length=1024)
    portfolioresume = ui.TextInput(label='Portfolio & Resume:', style=discord.TextStyle.paragraph,
                                   max_length=1024)
    aboutinfo = ui.TextInput(label='Tell us a bit about yourself:', style=discord.TextStyle.paragraph,
                             max_length=1024)
    whyapply = ui.TextInput(label='Why are you applying at ServerOwner?:', style=discord.TextStyle.paragraph,
                            max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
            applicationcat = discord.utils.get(interaction.guild.categories, id=1161821704457310279)
            if applicationcat:
                ticketchan = await interaction.guild.create_text_channel(
                    f"application-{interaction.user.name}", category=applicationcat,
                    overwrites=overwrites)

                await interaction.response.send_message(content=f"Application created in {ticketchan.mention}!",
                                                        ephemeral=True)
                await ticketchan.send(embed=await applicationembed(interaction.guild, interaction.user, self.nametz.value,
                                                                   self.applyfor.value, self.portfolioresume.value,
                                                                   self.aboutinfo.value, self.whyapply.value),
                                      view=applicationbuttonpanel())
        except Exception as e:
            print(e)


class applicationbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Application", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id=f"application:close")
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


class applicationbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Application", emoji="📩", style=discord.ButtonStyle.blurple,
                       custom_id=f"applicationbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"application-{interaction.user.name.lower()}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing application. {existticket.mention}",
                    ephemeral=True)
            else:
                await interaction.response.send_modal(Applicationmodal())
        except Exception as e:
            print(e)


class applicationcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="application", description="Command to create the application button")
    async def rtticket(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await interaction.response.send_message(f"Application button was sent to {channel.mention}", ephemeral=True)
            await channel.send(embed=applicationmessageembed(interaction.guild),
                               view=applicationbutton())
        except Exception as e:
            print(e)

    @rtticket.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(applicationcmd(bot))
    bot.add_view(applicationbutton())  # line that inits persistent view
    bot.add_view(applicationbuttonpanel())
