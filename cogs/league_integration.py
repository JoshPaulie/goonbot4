import os

import arrow
import cassiopeia as cass
import discord
import dotenv
from config import console
from discord.commands import Option, slash_command
from discord.ext import commands
from helpers.league.format_stat import format_stat as fstat
from helpers.league.parsers import LastGameParser

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

    @slash_command(name="lastgame")
    async def last_game(
        self,
        ctx: discord.ApplicationContext,
        summoner_name: Option(str, "Summoner name", autocomplete=get_goon_names),  # type: ignore
    ):
        """Check the last game of a given summoner!"""

        # QoL Variables
        summoner: cass.Summoner = cass.get_summoner(name=summoner_name, region="NA")
        last_game = LastGameParser(summoner)
        pipe_sep: str = " | "

        # Embed building

        lg_embed = discord.Embed(
            title=f"{summoner.name}'s last game",
            description=pipe_sep.join(
                [
                    f"{'**Victory!**' if last_game.match_outcome is True else '**Defeat.**'}",
                    fstat(arrow.get(last_game.match_end_time).humanize(), "match ended"),
                    fstat(f"{last_game.last_match.duration.seconds // 60}:{last_game.last_match.duration.seconds % 60}", "match duration"),
                ]
            ),
        )

        lg_embed.add_field(name="Final Score 🏁", value=pipe_sep.join(last_game.game_stats), inline=False)
        lg_embed.add_field(name="Teammates ⚓", value=pipe_sep.join(last_game.teammates), inline=False)
        lg_embed.add_field(name="Build 🏋️‍♂️", value=pipe_sep.join([*last_game.summoner_spells, *last_game.final_build]))
        lg_embed.add_field(name="Spell Count 🎯", value=pipe_sep.join(last_game.spells_used), inline=False)
        lg_embed.add_field(name="KDA Stats ⚔", value=pipe_sep.join(last_game.kda_stats), inline=False)
        lg_embed.add_field(name="Farm 👨‍🌾 & Vision Stats 👀", value=pipe_sep.join([*last_game.cs_stats, *last_game.vision_stats]), inline=False)
        lg_embed.add_field(name="Carry Stats 💪", value=pipe_sep.join(last_game.carry_stats), inline=False)

        if last_game.match_outcome:
            lg_embed.color = discord.Color.brand_green()
        else:
            lg_embed.color = discord.Color.brand_red()

        lg_embed.set_thumbnail(url=last_game.participant.champion.image.url)
        lg_embed.set_footer(text=last_game.match_queue_type.name.replace("_", " ").title())

        # Embed Sending
        await ctx.respond(embed=lg_embed)  # type: ignore


def setup(bot):
    bot.add_cog(League(bot))
