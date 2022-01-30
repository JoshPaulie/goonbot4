import discord
import discord.ext.commands
import dotenv
from config import both_servers
from discord.commands import slash_command
from discord.ext import commands
from helpers.special_dates import special_events_remaining

dotenv.load_dotenv()


class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @slash_command(guild_ids=both_servers)
    async def today(self, ctx: discord.ApplicationContext) -> None:
        """Returns if it's a special day, or when the next one will be"""
        next_event, next_event_days = special_events_remaining[0]
        second_event, second_event_days = special_events_remaining[1]

        event_embed = discord.Embed(color=discord.Color.blurple())
        if next_event_days == 0:
            event_embed.title = f"Today is {next_event}!"
        else:
            event_embed.title = f"{next_event} is in {next_event_days} days!"
            event_embed.description = f"...and {second_event} is in {second_event_days}"

        await ctx.respond(embed=event_embed)  # type: ignore


def setup(bot):
    bot.add_cog(Countdown(bot))
