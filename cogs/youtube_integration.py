import os

import arrow
import discord
import dotenv
from config import all_servers
from discord.commands import slash_command
from discord.ext import commands
from pyyoutube import Api

dotenv.load_dotenv()


class Youtube(commands.Cog, name="Youtube"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.yt_api = Api(api_key=os.getenv("GOOGLE"))

    def get_latest_video_url(self, channel_id: str):
        channel_info = self.yt_api.get_channel_info(channel_id=channel_id)
        uploads_playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads  # type: ignore
        playlist_items = self.yt_api.get_playlist_items(playlist_id=uploads_playlist_id, count=1)  # type: ignore
        lastest_upload_id = playlist_items.items[0].contentDetails.videoId  # type: ignore
        lastest_upload = self.yt_api.get_video_by_id(video_id=lastest_upload_id)  # type: ignore
        return f"https://www.youtube.com/watch?v={lastest_upload_id}"

    @slash_command(guild_ids=all_servers)
    async def campbell(self, ctx: discord.ApplicationContext):
        """Latest video by Dr. Soup 🍲"""
        await ctx.respond(self.get_latest_video_url("UCF9IOB2TExg3QIBupFtBDxg"))  # type: ignore

    @slash_command(guild_ids=all_servers)
    async def synapse(self, ctx: discord.ApplicationContext):
        """League 😲 moments"""
        await ctx.respond(self.get_latest_video_url("UCVw8WSz1c_cazwOA0Yk_P_w"))  # type: ignore


def setup(bot):
    bot.add_cog(Youtube(bot))
