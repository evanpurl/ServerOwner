import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands


async def assemblesuggestionembed(server, information, user, topic):
    embed = discord.Embed(title=f"ServerOwner | New Suggestion!",
                          description=f"""A new suggestion has been created by {user.mention}! What do you think of it?""",
                          color=discord.Color.orange(),
                          timestamp=datetime.datetime.now())

    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="Topic:", value=topic, inline=False)
    embed.add_field(name="Suggestion:", value=information, inline=False)
    embed.set_footer(text=f"©️ ServerOwner 2023")
    return embed


class suggestionmodal(ui.Modal, title='New Suggestion'):

    def __init__(self, bot, topic):
        super().__init__()
        self.bot = bot
        self.topic = topic
        self.channelid = 1160658144796618893  # Change after testing is done
        self.channel = None

    information = ui.TextInput(label='Suggestion Information:', style=discord.TextStyle.paragraph,
                               placeholder="N/A", required=True, max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.channel = discord.utils.get(interaction.guild.channels, id=self.channelid)
            msg = await self.channel.send(
                embed=await assemblesuggestionembed(interaction.guild, self.information, interaction.user, self.topic))

            await msg.add_reaction("<:ArrowUp:1162921040121434193>")
            await msg.add_reaction("<:ArrowDown:1162921041094508604>")

            await interaction.response.send_message(
                content=f"Suggestion created at {msg.jump_url}.",
                ephemeral=True)

        except Exception as e:
            print(e)


class suggestioncmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="suggest", description="Command used to create a suggestion.")
    @app_commands.choices(topic=[
        app_commands.Choice(name='General', value=1),
        app_commands.Choice(name='Discord', value=2),
        app_commands.Choice(name='Website', value=3),
        app_commands.Choice(name='Other', value=4),
    ])
    async def suggestion(self, interaction: discord.Interaction, topic: app_commands.Choice[int]):
        try:
            await interaction.response.send_modal(suggestionmodal(self.bot, topic.name))

        except Exception as e:
            print(e)

    @suggestion.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(suggestioncmd(bot))
