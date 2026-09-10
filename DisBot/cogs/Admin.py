import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f'Удалено {len(deleted)} сообщений.', delete_after=3)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass


async def setup(bot):
    await bot.add_cog(Admin(bot))