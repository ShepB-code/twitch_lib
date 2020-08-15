#Stream cog for twitch_bot

import discord
import itertools
from discord.ext import commands
import discord.utils

from twitch_lib import TwitchAPI

class Twitch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = TwitchAPI()
    
    def stream(self, user_name):
        stream_res = self.twitch.with_name_get_stream(user_name)

        streamer = [data['user_name'] for data in stream_res['data']][0]
        stream_game_id = [data['game_id'] for data in stream_res['data']][0]
        status = [data['type'] for data in stream_res['data']][0]
        title = [data['title'] for data in stream_res['data']][0]
        viewer_count = [data['viewer_count'] for data in stream_res['data']][0]
        stream_thumbnail = [data['thumbnail_url'] for data in stream_res['data']][0]

        return stream_game_id, title, viewer_count, stream_thumbnail

    def configure_thumbnail(self, thumbnail, width, height):
        configure_thumbnail = thumbnail.replace('{', '')
        configure_thumbnail = configure_thumbnail.replace('}', '')
        configure_thumbnail = configure_thumbnail.replace("width", str(width))
        configure_thumbnail = configure_thumbnail.replace('height', str(height))

        random_url_parameter = "?=" + "".join([random.choice(string.ascii_uppercase) + str(random.randint(0, 26)) for i in range(6)])

        return configure_thumbnail + random_url_parameter

    @commands.command()
    async def twitch(self, ctx, entered_name: str):

        #entered_name = args[0]
        

        channel_res = self.twitch.with_name_search_channel(entered_name)
        channel_display_names = [data['display_name'] for data in channel_res['data']]

        ##############################
        index_num = 0
        for name in channel_display_names:
            if name.upper() == entered_name.upper():
                channel_display_name = name
                channel_title = [data['title'] for data in channel_res['data']][index_num]
                channel_thumbnail = [data['thumbnail_url'] for data in channel_res['data']][index_num]
                channel_live_status = [data['is_live'] for data in channel_res['data']][index_num]

                found_channel = True

                break
                
            else:
                found_channel = False
                index_num += 1
        ##############################
        if found_channel == True: #Just incase the name that they entered doesn't exist.
        
            if channel_live_status:
                display_live_status = 'LIVE'
                use_stream_data = True


                stream_data = self.stream(channel_display_name)
                stream_game_id = stream_data[0]
                stream_title = stream_data[1]

                stream_viewer_count = stream_data[2]
                stream_thumbnail = stream_data[3]
                        

                game_res = self.twitch.with_id_get_game(stream_game_id)

                game_name = [data['name'] for data in game_res['data']][0]
                game_thumbnail = [data['box_art_url'] for data in game_res['data']][0]
            else:
                display_live_status = 'OFFLINE'
                use_stream_data = False
            ##############################

            shep_id = 498331656822849536

            ##############################
            #BASE EMBED 
            channel_url = f'https://www.twitch.tv/{channel_display_name}'
            channel_embed = discord.Embed(
                title=channel_display_name,
                url=channel_url,
                color=discord.Color.purple()
            )
            channel_embed.add_field(name='Status', value=display_live_status, inline=True)
            channel_embed.set_thumbnail(url=channel_thumbnail)
            channel_embed.set_footer(text='Made by Shep', icon_url=self.bot.get_user(shep_id).avatar_url)

            ##############################
            #CUSTOM EMBED (if channel is live)
            if use_stream_data:
                channel_embed.add_field(name='Game', value=game_name, inline=True)
                channel_embed.add_field(name='Viewer Count', value='{:,}'.format(stream_viewer_count), inline=True)
                channel_embed.add_field(name='Stream', value=f'[{stream_title}]({channel_url})', inline=False)

                channel_embed.set_image(url=self.configure_thumbnail(stream_thumbnail, 440, 248))
                
                
            ##############################
            await ctx.send(embed=channel_embed)


        else:
            await ctx.send(f"Couldn't find '{entered_name}'")
            

    
        

