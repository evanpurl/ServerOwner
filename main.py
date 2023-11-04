import os
import discord
import random
import json
import datetime
import sys
import asyncio
import platform

from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
from settings import *
from colorama import Fore

timestamp = datetime.datetime.now()

load_dotenv()

try:
    exec(open('settings.py').read())
except Exception as e:
    print(Fore.RED + '[!] Database Failure.' + Fore.RESET)

color = 0xfd83ff
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=".", case_insensitive=True, owner_id=int(os.environ.get('OWNERID')),
                      intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over ServerOwner"))


async def load_extensions(client):
    for filename in os.listdir("/home/container/cogs"):
        if filename.endswith(".py"):
            print(f"Loading Coroutine Object Generator (COG): {filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


error = discord.Color.from_rgb(255, 6, 0)
success = discord.Color.from_rgb(8, 255, 8)


async def main():
    async with client:
        await load_extensions(client)
        await client.start(os.getenv('token'))


asyncio.run(main())
