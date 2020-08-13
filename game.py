#Cog for the game command

import discord
import itertools
from discord.ext import commands
import discord.utils
import asyncio


from twitch_lib import TwitchAPI

class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = TwitchAPI()

    def configure_thumbnail(self, thumbnail, width, height):
        configure_thumbnail = thumbnail.replace('{', '')
        configure_thumbnail = configure_thumbnail.replace('}', '')
        configure_thumbnail = configure_thumbnail.replace("width", str(width))
        configure_thumbnail = configure_thumbnail.replace('height', str(height))

        return configure_thumbnail
    @commands.command()
    async def game(self, ctx, game: str):
        message = ctx.message
        shep_id = 498331656822849536



        #########################################
        game_res = self.twitch.with_name_get_game(game)


        game_id = [data['id'] for data in game_res['data']][0]
        game_name = [data['name'] for data in game_res['data']][0]
        game_thumbnail = [data['box_art_url'] for data in game_res['data']][0]
        '''
        configure_game_thumbnail = game_thumbnail.replace('{', '')
        configure_game_thumbnail = configure_game_thumbnail.replace('}', '')
        configure_game_thumbnail = configure_game_thumbnail.replace("width", '144')
        configure_game_thumbnail = configure_game_thumbnail.replace('height', '192')
'''
        #########################################
        stream_res = self.twitch.with_id_get_stream(game_id)

        stream_user_names = [data['user_name'] for data in stream_res['data']]
        stream_titles = [data['title'] for data in stream_res['data']]
        stream_viewer_counts = [data['viewer_count'] for data in stream_res['data']]
        stream_thumbnails = [data['thumbnail_url'] for data in stream_res['data']]


        
        #########################################
        embed = discord.Embed(
            title=f'Top 5 Streams for {game_name}',
            color=discord.Color.purple()
        )

        embed.add_field(name='Name', value=stream_user_names[0], inline=True)
        embed.add_field(name='Viewer Count', value=stream_viewer_counts[0], inline=True)
        embed.add_field(name='Stream', value=f'[{stream_titles[0]}](https://www.twitch.tv/{stream_user_names[0]})', inline=False)
        embed.set_image(url=self.configure_thumbnail(stream_thumbnails[0], 440, 248))
        embed.set_thumbnail(url=self.configure_thumbnail(game_thumbnail, 144, 192))
        embed.set_footer(text='Made by Shep', icon_url=self.bot.get_user(shep_id).avatar_url)

        embed_msg = await ctx.send(embed=embed)

        try:
            loop = True
            current_index = 0
            while loop:
                left_emoji = '⬅'
                right_emoji = '➡'
                exit_emoji = '❌'
                reaction_list = [left_emoji, right_emoji, exit_emoji]

                for emoji in reaction_list:
                    await embed_msg.add_reaction(emoji)

                def reaction_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in reaction_list

                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)

                if str(reaction) == left_emoji:
                    current_index -= 1
                
                elif str(reaction) == right_emoji:
                    current_index += 1
                
                elif str(reaction) == exit_emoji:
                    loop = False
                    inactive_embed = discord.Embed(
                        title='INACTIVE',
                        description='Exited by User',
                        color=discord.Color.red()
                    )
                    await embed_msg.edit(embed=inactive_embed)
                    
                    break
                if current_index > 4:
                    current_index = 0
                
                elif current_index < 0:
                    current_index = 4
                embed = discord.Embed(
                    title=f'Top 5 Streams for {game_name}',
                    color=discord.Color.purple()
                )

                embed.add_field(name='Name', value=stream_user_names[current_index], inline=True)
                embed.add_field(name='Viewer Count', value=stream_viewer_counts[current_index], inline=True)
                embed.add_field(name='Stream', value=f'[{stream_titles[current_index]}](https://www.twitch.tv/{stream_user_names[current_index]})', inline=False)
                embed.set_image(url=self.configure_thumbnail(stream_thumbnails[current_index], 440, 248))
                embed.set_thumbnail(url=self.configure_thumbnail(game_thumbnail, 144, 192))
                embed.set_footer(text='Made by Shep', icon_url=self.bot.get_user(shep_id).avatar_url)


                await embed_msg.edit(embed=embed)
        except asyncio.TimeoutError:
            inactive_embed = discord.Embed(
                title='INACTIVE',
                description='Timeout Error',
                color=discord.Color.red()
            )
            await embed_msg.edit(embed=inactive_embed)

                

                
                

    


