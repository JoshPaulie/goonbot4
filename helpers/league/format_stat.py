def format_stat(stat: str | int | float, description: str | int) -> str:
    """Formats stat and desc into discord's markdown"""

    if isinstance(stat, int):
        stat = f"{stat:,d}"

    return f"**{stat}** {description}"
