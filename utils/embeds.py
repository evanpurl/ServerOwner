import discord
from datetime import datetime


async def user_warning_embed(user, reasons):
    embed = discord.Embed(title=f"ServerOwner | {user.name}'s Warnings",
                          color=discord.Color.orange())
    embed.set_thumbnail(url=user.guild.icon.url)
    if len(reasons) > 25:
        embed.add_field(name=f"ServerOwner | Limit Exceeded!",
                        value=f"The number of warnings you've given this member exceeds 25, which is the maximum number of fields Discord allows in an embed.")
        return embed
    for index, value in enumerate(reasons):
        embed.add_field(name=f"Warning {index + 1}", value=value[0])
    return embed


async def user_warned_embed(user, reason, number):
    embed = discord.Embed(title=f"ServerOwner | New Warning!",
                          color=discord.Color.orange())
    embed.set_thumbnail(url=user.guild.icon.url)
    embed.add_field(name=f"Reason for Warning:", value=reason)
    if number:
        embed.add_field(name=f"Warning Count:", value=number)
    return embed


async def log_embed(description, logname, logdata, bot):
    embed = discord.Embed(
        title=f"{logname}", color=discord.Color.orange(), timestamp=datetime.now(),
        description=description)
    for index, value in enumerate(logdata):
        embed.add_field(name=logdata[index][0], value=logdata[index][1], inline=False)
    embed.set_thumbnail(url=bot.user.avatar)
    embed.set_footer(text=f"© ServerOwner 2023")
    return embed
