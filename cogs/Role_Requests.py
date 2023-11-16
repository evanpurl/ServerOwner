import discord
from discord import app_commands, ui
from discord.ext import commands

requestchannel = 1174790968818544650


async def requestembed(server, user, resume, active_servers, mc_username, role_to_request):
    try:

        embed = discord.Embed(title=f"ServerOwner | New Request!",
                              description=f"""A new request has been submitted by {user.mention}.""",
                              color=discord.Color.orange())
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name=f"Role Requested:", value=role_to_request, inline=False)
        embed.add_field(name=f"Minecraft Username:", value=mc_username, inline=False)
        embed.add_field(name=f"Resume or CV:", value=resume, inline=False)
        embed.add_field(name=f"Active Servers:", value=active_servers, inline=False)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


class requestmodal(ui.Modal, title='ServerOwner Role Request Form'):

    def __init__(self, bot, role):
        super().__init__()
        self.bot = bot
        self.role = role

    mc_username = ui.TextInput(label='Minecraft Username:', style=discord.TextStyle.paragraph, max_length=1024)
    resume = ui.TextInput(label='Resume or CV:', style=discord.TextStyle.paragraph, max_length=1024)
    active_servers = ui.TextInput(label='Active Server Links:', style=discord.TextStyle.paragraph,
                                  max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Gets channel object
            channel = discord.utils.get(interaction.guild.channels, id=requestchannel)
            # Sends request to channel
            await channel.send(
                embed=await requestembed(interaction.guild, interaction.user, self.resume, self.active_servers, self.mc_username, self.role))
            # Notifies user that request is sent.
            await interaction.response.send_message(
                content=f"Your request has been sent, please wait while we review your info.",
                ephemeral=True)
        except Exception as e:
            print(e)


class role_request_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="request_role", description="Command to request a role.")
    @app_commands.choices(role=[
        app_commands.Choice(name='Server Owner', value=1),
        app_commands.Choice(name='Server Manager', value=2),
        app_commands.Choice(name='Server Administrator', value=3),
        app_commands.Choice(name='Server Developer', value=4),
        app_commands.Choice(name='Server Staff', value=5),
        app_commands.Choice(name='Server Hosting', value=6),
        app_commands.Choice(name='Service Provider', value=7),
        app_commands.Choice(name='Builder', value=8),
        app_commands.Choice(name='Artist', value=9),
    ])
    async def role_request(self, interaction: discord.Interaction, role: app_commands.Choice[int]) -> None:
        try:

            await interaction.response.send_modal(requestmodal(self.bot, role.name))
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="accept", description="Command to add a user to a role")
    async def accept(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role) -> None:
        try:
            if role not in user.roles:
                await user.add_roles(role)
                await interaction.response.send_message(content=f"{user.mention} has been added to role {role.mention}.")
            else:
                await interaction.response.send_message(
                    content=f"{user.mention} is already in role {role.mention}.")
        except Exception as e:
            print(e)

    @role_request.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(role_request_cmd(bot))
