import discord
import os

os.environ['OWNERID'] = '979797311792222208'  # Qezy
os.environ['BOT_TOKEN'] = 'Hidden'
os.environ['BOT_DB'] = 'MySQL'
os.environ['BOT_VERSION'] = 'v0.01'


# EMBED HELPER
def create_embed(text):
    embed = discord.Embed(
        description=text,
        colour=discord.Colour.from_rgb(136, 3, 252),
    )
    return embed
