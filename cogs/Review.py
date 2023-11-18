import discord
from discord import app_commands, ui
from discord.ext import commands

verifiedchannel = 1160657305562533899
unverifiedchannel = 1160657320934645790

verifiedroles = [1155530172997566511, 1159314544347324466, 1159314541381959710]  # Reputable 1, 2, 3


async def reviewembed(server, user, origuser, rating, detailedreview):
    try:
        star = "⭐"
        if not isinstance(int(rating.value), int):
            rate = 5 * star
        else:
            rate = int(rating.value) * star
        embed = discord.Embed(title=f"ServerOwner | New Review!",
                              description=f"""A new review has been created by {origuser.mention}.""",
                              color=discord.Color.orange())
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name=f"Discord Username:", value=user.mention, inline=False)
        embed.add_field(name=f"User Rating:", value=rate, inline=False)
        embed.add_field(name=f"Detailed Review:", value=detailedreview, inline=False)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


class Reviewmodal(ui.Modal, title='New Review'):

    def __init__(self, user):
        super().__init__()
        self.user = user

    userrating = ui.TextInput(label='List your rating from 1-5', style=discord.TextStyle.short,
                              max_length=1)
    detailedreview = ui.TextInput(label='Detailed Review:', style=discord.TextStyle.paragraph,
                                  max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        if any(role.id in verifiedroles for role in interaction.user.roles):  # looks for role id in user's roles.
            channel = discord.utils.get(interaction.guild.channels, id=verifiedchannel)
            await channel.send(embed=await reviewembed(interaction.guild, self.user, interaction.user, self.userrating, self.detailedreview))
            await interaction.response.send_message(content=f"Your review has been posted in {channel.mention}", ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, id=unverifiedchannel)
            await channel.send(embed=await reviewembed(interaction.guild, self.user, interaction.user, self.userrating,
                                                       self.detailedreview))
            await interaction.response.send_message(content=f"Your review has been posted in {channel.mention}", ephemeral=True)


class reviewcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="review", description="Command used to create a review.")
    async def review(self, interaction: discord.Interaction, user: discord.Member) -> None:
        try:
            if interaction.user.id == user.id:
                await interaction.response.send_message(content=f"You can't review yourself.", ephemeral=True)
            else:
                await interaction.response.send_modal(Reviewmodal(user))
        except Exception as e:
            print(e)

    @review.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(reviewcmd(bot))
