import discord
import os
from discord import app_commands
from discord.ext import commands


class Informationcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="info", description="Command to load information from a file")
    async def info(self, interaction: discord.Interaction, channel: discord.TextChannel, file_name: str,
                   embed_title: str):
        try:
            if os.path.exists(f"storage/info/{file_name}.txt"):
                with open(f"storage/info/{file_name}.txt", 'r') as f:
                    data = f.read()
                await interaction.response.send_message(content=f"File data loaded in channel {channel.mention}!",
                                                        ephemeral=True)
                await channel.send(embed=await assembleembed(interaction.guild, data, embed_title))
            else:
                await interaction.response.send_message(content=f"File not found.", ephemeral=True)

        except Exception as e:
            print(e)


async def assembleembed(server, data, title):
    try:
        embed = discord.Embed(title=title,
                              description=data,
                              color=discord.Color.orange())
        embed.set_thumbnail(url=server.icon.url)
        embed.set_footer(text=f"© ServerOwner 2023")
        return embed
    except Exception as e:
        print(e)


async def setup(bot):
    await bot.add_cog(Informationcmd(bot))
