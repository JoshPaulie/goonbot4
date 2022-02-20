import discord
from config import console
from discord.commands import slash_command
from discord.ext import commands


class Listeners(commands.Cog, name="listeners"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     """Made for reference"""
    #     if "test" in message.content:
    #         await message.reply("You said test!")


def setup(bot):
    bot.add_cog(Listeners(bot))
