#Discord Twitch Bot
import discord
import itertools
from discord.ext import commands
import discord.utils

from twitch_lib import TwitchAPI
import twitch
import game


bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('?info for commands'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

bot.add_cog(twitch.Twitch(bot))
bot.add_cog(game.Game(bot))

with open('BOT_TOKEN.txt', 'r') as f:
    bot.run(f.read().strip())