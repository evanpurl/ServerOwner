import discord


async def user_warning_embed(user, reasons):
    embed = discord.Embed(title=f"**{user.name}'s Warnings**",
                          color=discord.Color.orange())
    embed.set_thumbnail(url=user.guild.icon.url)
    if len(reasons) > 25:
        embed.add_field(name=f"Warning Message",
                        value=f"The number of warnings that you gave this member exceeds 25, which is the max number of fields that discord allows in an embed.")
        return embed
    for index, value in enumerate(reasons):
        embed.add_field(name=f"Warning {index + 1}", value=value[0])
    return embed


async def user_warned_embed(user, reason, number):
    embed = discord.Embed(title=f"**{user.guild.name} Warning**",
                          color=discord.Color.orange())
    embed.set_thumbnail(url=user.guild.icon.url)
    embed.add_field(name=f"Reason for warning", value=reason)
    if number:
        embed.add_field(name=f"Warning Number", value=number)
    return embed


async def log_embed(logname, logdata, bot):
    embed = discord.Embed(
        title=f"{logname}", color=discord.Color.orange())
    for index, value in enumerate(logdata):
        embed.add_field(name=logdata[index][0], value=logdata[index][1])
    embed.set_thumbnail(url=bot.user.avatar)
    return  embed
