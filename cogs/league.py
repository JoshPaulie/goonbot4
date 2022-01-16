import cassiopeia
import discord
from config import both_servers
from discord.commands import Option, slash_command
from discord.ext import commands

SUMMONER_NAMES = [
    "bexli",
    "mltsimpleton",
    "ectoplax",
    "roninalex",
    "artificialmeat",
    "large frog tamer",
    "boxrog",
    "vynle",
    "poydok",
    "cradmajone",
]


async def get_names(ctx: discord.AutocompleteContext):
    """Returns a list of names that begin with the characters entered so far."""
    return sorted([name for name in SUMMONER_NAMES if name.startswith(ctx.value.lower())])


class League(commands.Cog, name="League"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @slash_command(guild_ids=both_servers)
    async def last_game(
        self,
        ctx,
        summoner_name: Option(str, "Summoner name", autocomplete=get_names),
    ):
        """Heavy development, basically unstarted"""
        await ctx.respond(f"This is in dev. You picked {summoner_name}")


def setup(bot):
    bot.add_cog(League(bot))
