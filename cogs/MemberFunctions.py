import datetime
import discord

from discord.ext import commands
from settings import *


class MemberFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel_id = 1158943373533659279
            role_id = 1155530173010169890

            channel = discord.utils.get(member.guild.channels, id=channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"<:Envelope:1155545837854793859> Welcome to ServerOwner, {member.name}!",
                    description=f"Our platform is designed to foster collaboration, promote services and projects, and facilitate interactions within our fantastic community. It's worth noting that our community is semi-private, so you'll need to have a designated role to access specific channels.\n\n**Information:**\n<:Twitter:1158944250210291814> **Twitter:** https://twitter.com/serverownergg\n<:Globe:1158944467886276648> **Website:** https://serverowner.gg/",
                    color=discord.Color.orange(),
                    timestamp=datetime.datetime.now()
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text=f"© ServerOwner 2023")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/1143318907252392007/1158945150609928252/ENfQtWi.png?ex=651e1748&is=651cc5c8&hm=de055456567b3ff905bb21635c18dcf96a5756f5587e436eb758dd754790495d&")
                await channel.send(embed=embed)

            role = discord.utils.get(member.guild.roles, id=role_id)
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(MemberFunctions(bot))
