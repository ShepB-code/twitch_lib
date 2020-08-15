#Cog for the game command

import discord
import itertools
from discord.ext import commands
import discord.utils
import asyncio
import time

from twitch_lib import TwitchAPI

class Pete(commands.Cog):

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
    async def pete(self, ctx, *game: str):

        message = ctx.message
        shep_id = 498331656822849536

        spaced_game  = ' '.join(game)

        #game_url_form = '%20'.join(game) #if there are mutiple entries in game
        
        

        try:
            #########################################

            search_res = self.twitch.with_name_search_category(spaced_game)
            
            start_time = time.time()
            game_ids = [data['id'] for data in search_res['data']]
            print("After getting game_ids:", time.time() - start_time)

            
            start_time = time.time()
            game_ids.sort(reverse=True, key=lambda game_id : len(self.twitch.with_id_get_stream(game_id)["data"]))
            print("After sorting:", time.time() - start_time)

            start_time = time.time()
            games = [self.twitch.with_id_get_game(game_id)["data"][0] for game_id in game_ids]
            game_names_list = [game["name"] for game in games]
            game_thumbnails_list = [game["box_art_url"] for game in games]
            print("After 3 game loops:", time.time() - start_time)


            start_time = time.time()
            found_game = False
            # TODO make less lines
            for name in game_names_list:
                # Not sure what this is about gtg
                if spaced_game.upper() == name.upper():
                    game_name = name
                    current_game = self.twitch.with_name_get_game(name)["data"][0]
                    game_id = current_game["id"]
                    game_thumbnail = current_game['box_art_url']
                    found_game = True   
                    break   
            print("After if statment for names:", time.time() - start_time)

            if not found_game:
                start_time = time.time()
                
                one_emoji = '1️⃣'
                two_emoji = '2️⃣'
                three_emoji = '3️⃣'
                four_emoji = '4️⃣'
                five_emoji = '5️⃣'
                find_game_emoji_dict = {one_emoji: 0, two_emoji:1, three_emoji:2, four_emoji:3, five_emoji:4}

                find_name_embed = discord.Embed(
                    title='Did you mean...',
                    color=discord.Color.orange()
                )
                find_name_embed.add_field(name=one_emoji, value=game_names_list[0], inline=False)
                find_name_embed.add_field(name=two_emoji, value=game_names_list[1], inline=False)
                find_name_embed.add_field(name=three_emoji, value=game_names_list[2], inline=False)
                find_name_embed.add_field(name=four_emoji, value=game_names_list[3], inline=False)
                find_name_embed.add_field(name=five_emoji, value=game_names_list[4], inline=False)

                find_name_msg = await ctx.send(embed=find_name_embed)
                
                for emoji in find_game_emoji_dict.keys():
                    await find_name_msg.add_reaction(emoji)
                print("After embed:", time.time() - start_time)

                def find_name_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in find_game_emoji_dict.keys()
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=find_name_check)
                    
                    game_name = game_names_list[find_game_emoji_dict[str(reaction)]]
                    game_id = game_ids[find_game_emoji_dict[str(reaction)]]
                    game_thumbnail = game_thumbnails_list[find_game_emoji_dict[str(reaction)]]
                except asyncio.TimeoutError:
                    find_name_embed.color = discord.Color.dark_grey() #Grey color 
                    await find_name_msg.edit(embed=find_name_embed)
    
                
                
                

            
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
                    reaction_list = [left_emoji, right_emoji]

                    for emoji in reaction_list:
                        await embed_msg.add_reaction(emoji)

                    def reaction_check(reaction, user):
                        return user == message.author and str(reaction.emoji) in reaction_list

                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)

                    if str(reaction) == left_emoji:
                        current_index -= 1
                    
                    elif str(reaction) == right_emoji:
                        current_index += 1
                    
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
                embed.color = discord.Color.dark_grey() #Grey color 
                await embed_msg.edit(embed=embed)
        except IndexError:
            await ctx.send(f'No streams were found for {game_name} ☹')
                  
                
                
                
                
                
                
                
                
                
                
                
                