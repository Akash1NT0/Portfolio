import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default() 
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} успешно запущен!')
    print(f'Бот состоит на {len(bot.guilds)} серверах:')
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

async def main():

    await bot.load_extension('cogs.moderation')
    if TOKEN is None:
        print("Ошибка: Токен не найден. Проверьте файл .env")
    else:
        bot.run(TOKEN)

bot.command(name='load')
@commands.is_owner() # Только владелец бота может это делать
async def load_ext(ctx, extension: str):

    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение `{extension}` загружено.')
    except Exception as e:
        await ctx.send(f'Ошибка загрузки `{extension}`: {e}')

@bot.command(name='unload')
@commands.is_owner()
async def unload_ext(ctx, extension: str):

    try:
        await bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение `{extension}` выгружено.')
    except Exception as e:
        await ctx.send(f'Ошибка выгрузки `{extension}`: {e}')

@bot.command(name='reload')
@commands.is_owner()
async def reload_ext(ctx, extension: str):

    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение `{extension}` перезагружено.')
    except Exception as e:
        await ctx.send(f'Ошибка перезагрузки `{extension}`: {e}')

import asyncio
asyncio.run(main())