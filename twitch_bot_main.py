#Discord Twitch Bot
import discord
import itertools
from discord.ext import commands
import discord.utils

from twitch_lib import TwitchAPI
import twitch

TOKEN = 'NzM4MjAyNjYwMjI1Njc5NDAx.XyIezQ.K-a5oiZ8Pcvu90Ci77jXfuMzeTU'

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('?info for commands'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

bot.add_cog(twitch.Twitch(bot))
bot.run(TOKEN)