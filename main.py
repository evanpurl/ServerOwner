import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from utils.loading import load_extensions

load_dotenv()
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)
client.remove_command("help")


async def main():
    async with client:
        await load_extensions(client)
        await client.start(os.getenv('token'))


asyncio.run(main())
