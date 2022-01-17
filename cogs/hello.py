from discord.commands import Option, slash_command
from discord.ext import commands


class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[510865274594131968])
    async def hello(self, ctx, name: Option(str, "Enter your name")):
        """Say hello to the bot"""  # the command description can be supplied as the docstring
        await ctx.respond(f"Hello {name}!")


def setup(bot):
    bot.add_cog(HelloCog(bot))
