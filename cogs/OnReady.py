import os

import discord
from discord.ext import commands

from utils.sqlite import ticket


class onreadyfunction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await ticket()
        if not os.path.exists(f"storage/info/"):
            os.makedirs(f"storage/info/")
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"over ServerOwner"))
        print(f'We have logged in as {self.bot.user.name}')


async def setup(client):
    await client.add_cog(onreadyfunction(client))
