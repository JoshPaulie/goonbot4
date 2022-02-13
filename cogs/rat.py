import random

import discord
from discord.commands import slash_command
from discord.ext import commands


class Rat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rats = self.rat_images()
        self.caged_rats = []

    @staticmethod
    def rat_images() -> list:
        with open("text_files/rats.txt") as links:
            rats = links.read().splitlines()
            return rats

    def check_rat_capacity(self):
        if len(self.rats) == 0:
            self.rats = self.caged_rats
            self.caged_rats = []

    @slash_command()
    async def rat(self, ctx: discord.ApplicationContext):
        """Random rat"""
        chosen_rat = random.choice(self.rats)
        self.rats.remove(chosen_rat)
        self.caged_rats.append(chosen_rat)
        await ctx.respond(embed=discord.Embed(title="Rat", color=discord.Color.blurple()).set_image(url=chosen_rat))  # type: ignore
        self.check_rat_capacity()


def setup(bot):
    bot.add_cog(Rat(bot))
