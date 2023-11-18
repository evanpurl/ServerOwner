from discord.ext import commands


class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def sync(self, ctx):
        try:
            if ctx.author.id == 979797311792222208 or 228674682889437184:
                print(f"Syncing commands")
                await self.client.tree.sync()
                await ctx.send(f"Commands synced")
                print(f"Commands synced")
            else:
                await ctx.send(f"You do not have permission to run this command.")
        except Exception as e:
            await ctx.send(str(e))

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f"I've successfully loaded the {extension} extension!")
        except Exception as e:
            print(f"I have received an error while loading the {extension} cog. Error: {e}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            self.client.unload_extension(f'cogs.{extension}')
            await ctx.send(f"I've successfully unloaded the {extension} extension!")
        except Exception as e:
            print(f"I have received an error while unloading the {extension} cog. Error: {e}")


async def setup(client):
    await client.add_cog(System(client))
