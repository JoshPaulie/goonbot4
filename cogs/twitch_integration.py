import os

import arrow
import discord
import dotenv
import twitch
from discord.commands import slash_command
from discord.ext import commands

dotenv.load_dotenv()


class Twitch(commands.Cog, name="Twitch"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.ttv = twitch.Helix(os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET"))  # type: ignore

    def make_ttv_embed(self, ttv_username) -> discord.Embed:
        link_embed = discord.Embed(color=discord.Color.blurple())
        ttv_username = self.ttv.user(ttv_username)
        if ttv_username is not None:
            link_embed.url = f"https://www.twitch.tv/{ttv_username.display_name}"
            if ttv_username.is_live:
                link_embed.title = f"{ttv_username.display_name} is live!"
                link_embed.set_thumbnail(url=ttv_username.profile_image_url)
                link_embed.description = "\n".join(
                    [
                        ttv_username.stream.title,
                        f"*Began {arrow.get(ttv_username.stream.started_at).humanize()}*",
                    ]
                )
            else:
                link_embed.title = f"{ttv_username.display_name} is offline 😌"
                link_embed.set_thumbnail(url=ttv_username.offline_image_url)
        else:
            link_embed.title = "The username you search doesn't exist"
            link_embed.description = "*Is it possible they changed their name, or was banned?*"

        return link_embed

    @slash_command()
    async def dekar(self, ctx: discord.ApplicationContext):
        """Link to Dekar's stream"""
        await ctx.respond(embed=self.make_ttv_embed("dekar173"))  # type: ignore

    @slash_command()
    async def jerma(self, ctx: discord.ApplicationContext):
        """Link to Jerma's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("jerma985"))  # type: ignore

    @slash_command()
    async def tyler1(self, ctx: discord.ApplicationContext):
        """Link to Tyler's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("loltyler1"))  # type: ignore

    @slash_command()
    async def happy_hob(self, ctx: discord.ApplicationContext):
        """Link to The Happy Hob's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("the_happy_hob"))  # type: ignore

    @slash_command()
    async def dangheesling(self, ctx: discord.ApplicationContext):
        """Link to Tyler's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("dangheesling"))  # type: ignore

    @slash_command()
    async def dunkstream(self, ctx: discord.ApplicationContext):
        """Link to Dunkey's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("dunkstream"))  # type: ignore

    @slash_command()
    async def thebausffs(self, ctx: discord.ApplicationContext):
        """Link to Babus's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("thebausffs"))  # type: ignore

    @slash_command()
    async def northernlion(self, ctx: discord.ApplicationContext):
        """Link to Northernlion's Stream"""
        await ctx.respond(embed=self.make_ttv_embed("northernlion"))  # type: ignore


def setup(bot):
    bot.add_cog(Twitch(bot))
