import os

import arrow
import cassiopeia as cass
import discord
import dotenv
from discord.commands import Option, slash_command
from discord.ext import commands
from helpers.league.calculators import calc_kda
from helpers.league.format_stat import format_stat as fstat
from helpers.league.parsers import LastGameParser, LastTeamParser, SummonerLookup

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


pipe_sep: str = " | "


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

    @slash_command(name="lastteam")
    async def last_team(
        self,
        ctx: discord.ApplicationContext,
        summoner_name: Option(str, "Summoner name", autocomplete=get_goon_names),  # type: ignore
    ):
        """Josh's troll analysis"""
        summoner: cass.Summoner = cass.get_summoner(name=summoner_name, region="NA")
        last_team = LastTeamParser(summoner)

        lt_embed = discord.Embed(title="Last team", description="Under development")
        for teammate in last_team.last_teammates:
            troll_stats = last_team.make_troll_stats(teammate.stats)
            if troll_stats:
                lt_embed.add_field(name=teammate.summoner.name, value=pipe_sep.join(last_team.make_troll_stats(teammate.stats)), inline=False)
            else:
                lt_embed.add_field(name=teammate.summoner.name, value="🤐", inline=True)

        await ctx.respond(embed=lt_embed)  # type: ignore

    @slash_command(name="who")
    async def who(
        self,
        ctx: discord.ApplicationContext,
        summoner_name: Option(str, "Summoner name", autocomplete=get_goon_names),  # type: ignore
    ):
        """Not working!"""
        summoner: cass.Summoner = cass.get_summoner(name=summoner_name, region="NA")
        lookup_results = SummonerLookup(summoner=summoner)

        who_embed = discord.Embed(title=summoner.name)

        summ_rank_fives = summoner.league_entries.fives
        who_embed.add_field(name="Fives Rank", value=summ_rank_fives)
        await ctx.respond(embed=who_embed)  # type: ignore


def setup(bot):
    bot.add_cog(League(bot))
