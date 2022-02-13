import random

import discord
from config import all_servers
from discord.commands import Option, slash_command
from discord.ext import commands


class Affirmations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def ily(self, ctx: discord.ApplicationContext, name: Option(discord.Member, "@Mention the Goon you love")):  # type: ignore
        """Tell someone you love them!"""
        emotes = ["😍", "😘", "🥰", "🤩", "🤗", "❤", "💕", "💞", "🖤"]
        await ctx.respond(f"I love you, {name}! {random.choice(emotes)}")  # type: ignore


def setup(bot):
    bot.add_cog(Affirmations(bot))
