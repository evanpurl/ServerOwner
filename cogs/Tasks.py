import os
from datetime import datetime
from utils.sqlite import get_alltickets, create_db, remove
import discord
from discord.ext import commands, tasks
import chat_exporter, io

guildid = 1155530172997566506


class tasksfile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not os.path.exists(f"storage/"):
            os.makedirs(f"storage/")
        if not self.checktickets.is_running():
            self.checktickets.start()

    @tasks.loop(minutes=30)
    async def checktickets(self):
        try:
            conn = await create_db(f"storage/tickets.db")
            for a in await get_alltickets(conn):
                if a[2]:
                    time_till = datetime.strptime(a[2], '%Y-%m-%d %H:%M:%S.%f') - datetime.now()
                    if time_till.total_seconds() <= 0:
                        guild = self.bot.get_guild(guildid)
                        logchannel = discord.utils.get(guild.channels,
                                                       id=1155617191828410418)
                        if logchannel:
                            channel = discord.utils.get(guild.channels, id=int(a[1]))
                            user = self.bot.get_user(int(a[0]))
                            print(f"Closing ticket from user {user.name}")
                            transcriptdm = await chat_exporter.export(
                                channel,
                            )
                            transcripttochannel = await chat_exporter.export(
                                channel,
                            )
                            if transcriptdm is None:
                                return
                            if transcripttochannel is None:
                                return

                            transcript_file_to_dm = discord.File(
                                io.BytesIO(transcriptdm.encode()),
                                filename=f"transcript-{channel.name}.html",
                            )
                            transcript_file_to_channel = discord.File(
                                io.BytesIO(transcripttochannel.encode()),
                                filename=f"transcript-{channel.name}.html",
                            )

                            await user.send(file=transcript_file_to_dm)
                            await logchannel.send(file=transcript_file_to_channel)

                            await channel.delete()
                            await remove(conn, user)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(tasksfile(bot))
