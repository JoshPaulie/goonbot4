"""
This cog is broken for whatever reason.
The expection simply says 'Bot' object has no attribute 'all_commands', which is odd because it seems no different from the other cogs.
"""
import random
import discord

from config import both_servers
from discord.commands import slash_command
from discord.ext import commands


class Rat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rats = self.rat_images()
        self.caged_rats = []

    @staticmethod
    def rat_images() -> list:
        with open("cogs_helpers/rats.txt") as links:
            rats = links.read().splitlines()
            return rats

    def check_rat_capacity(self):
        if len(self.rats) == 0:
            self.rats = self.caged_rats
            self.caged_rats = []

    @slash_command(guild_ids=both_servers)
    async def rat(self, ctx):
        """Random rat"""
        chosen_rat = random.choice(self.rats)
        self.rats.remove(chosen_rat)
        self.caged_rats.append(chosen_rat)
        await ctx.respond(
            embed=discord.Embed(title="Rat", color=discord.Color.blurple()).set_image(chosen_rat)
        )
        self.check_rat_capacity()


def setup(bot):
    bot.add_cog(Rat(bot))
