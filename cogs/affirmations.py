import random

import discord
from discord.commands import Option, slash_command
from discord.ext import commands

from config import both_servers


class Affirmations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=both_servers)
    async def ily(self, ctx, name: Option(discord.Member, "@Mention the Goon you love")):
        """Tell someone you love them!"""
        emotes = ["😍", "😘", "🥰", "🤩", "🤗", "❤", "💕", "💞", "🖤"]
        await ctx.respond(f"I love you, {name}! {random.choice(emotes)}")


def setup(bot):
    bot.add_cog(Affirmations(bot))
