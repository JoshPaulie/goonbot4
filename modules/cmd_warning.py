import discord
import discord.ext.commands


async def development_warning(ctx: discord.ext.commands.Context):
    warn_embed = discord.Embed(
        title="Under construction! 🚧",
        description="This command may not work as expected.",
        color=discord.Color.blurple(),
    )
    await ctx.send(embed=warn_embed, delete_after=8)
