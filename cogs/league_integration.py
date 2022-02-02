import os

import arrow
import cassiopeia as cass
import discord
import dotenv
from config import all_servers
from discord.commands import Option, slash_command
from discord.ext import commands
from helpers.league.parsers import LastGameParser
from modules.cmd_warning import development_warning

GOON_SUMMONER_NAMES = [
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

dotenv.load_dotenv()
cass.set_riot_api_key(os.getenv("RIOT"))  # type: ignore


async def get_goon_names(ctx: discord.AutocompleteContext):
    """Returns a list of names that begin with the characters entered so far."""
    return sorted([name for name in GOON_SUMMONER_NAMES if name.startswith(ctx.value.lower())])


class League(commands.Cog, name="League"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @slash_command(guild_ids=all_servers, name="lastgame")
    async def last_game(
        self,
        ctx: discord.ApplicationContext,
        summoner_name: Option(str, "Summoner name", autocomplete=get_goon_names),  # type: ignore
    ):
        """Check the last game of a given summoner!"""

        # QoL Variables
        summoner = cass.get_summoner(name=summoner_name, region="NA")
        last_game = LastGameParser(summoner)

        # Embed building

        lg_embed = discord.Embed(
            title=f"{summoner.name}'s last game",
            description=" | ".join(
                [
                    f"Match ended {arrow.get(last_game.match_end_time).humanize()}",
                    f"{'Victory!' if last_game.match_outcome is True else 'Defeat.'}",
                ]
            ),
        )

        lg_embed.add_field(
            name="Team mates ⚓",
            value=" | ".join(
                [
                    teammate.summoner.name
                    for teammate in last_game.participant_team.participants
                    if teammate.summoner.name != summoner.name
                ]
            ),
            inline=False,
        )
        lg_embed.add_field(name="KDA Stats ⚔", value="\n".join(last_game.kda_stats()))
        lg_embed.add_field(name="CS Stats 👨‍🌾", value="\n".join(last_game.cs_per_min_stats()))
        lg_embed.add_field(name="Carry Stats 💪", value="\n".join(last_game.damage_dealt_stats()))

        if last_game.match_outcome:
            lg_embed.color = discord.Color.brand_green()
        else:
            lg_embed.color = discord.Color.brand_red()

        lg_embed.set_footer(text=last_game.match_queue_type.name.replace("_", " "))

        # Embed Sending
        await ctx.respond(embed=lg_embed)  # type: ignore
        await development_warning(ctx)


def setup(bot):
    bot.add_cog(League(bot))
