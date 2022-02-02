def calc_kda(kills: int, deaths: int, assists: int) -> str | float:
    """Handles KDA with no deaths"""
    if not deaths:
        return "PERF 👑"
    else:
        return (kills + assists) / deaths


def calc_participant_percent(participant_stat: int | float, team_stat: int | float) -> str:
    """Compares a participants stats to the team's as a whole"""
    return f"{round((participant_stat / team_stat) * 100)}%"
