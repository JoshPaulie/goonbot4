import os
import random

import discord
from config import all_servers
from discord.commands import Option, slash_command
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=all_servers)
    async def pfp(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "Pick a goon to fetch pfp") = None):  # type: ignore
        """GOON BOT BEATS BONGO 1000:1"""
        if user is None:
            selected_user = ctx.author
        else:
            selected_user = user

        pfp_url = selected_user.display_avatar.url

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(name=f"{selected_user.name} 📸", url=pfp_url)
        embed.set_image(url=pfp_url)
        await ctx.respond(embed=embed)  # type: ignore

    @slash_command(guild_ids=all_servers)
    async def vtuber(self, ctx: discord.ApplicationContext):
        """Better than ever!"""
        await ctx.send("🤫", delete_after=1)

    @slash_command(guild_ids=all_servers)
    async def coinflip(self, ctx: discord.ApplicationContext):
        """Gives you heads or tails"""
        coin = random.choice(["Heads", "Tails"])
        await ctx.respond(embed=discord.Embed(title=coin, color=discord.Color.blurple()))  # type: ignore

    @slash_command(guild_ids=all_servers)
    async def wni(self, ctx: discord.ApplicationContext):
        """Wow, no invite?"""
        complaint = random.choice(
            [
                "Wow, no invite?",
                "WOW..no invite?",
                "My invite must have gotten lost in the mail",
                "Wow no invite?",
                "WOW. NOT INVITED, NOT SURPRISED.",
                "WOW. NO INVITE, NOT SURPRISED.",
                "come on man not cool",
                "i thought we were friends",
                "guess ill hangout here... alone... again",
                "hey, come on! I like darts too",
            ]
        )
        await ctx.respond(embed=discord.Embed(title=complaint, color=discord.Color.blurple()))  # type: ignore


def setup(bot):
    bot.add_cog(General(bot))
