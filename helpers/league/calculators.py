import cassiopeia as cass


def calc_kda(kills: int, deaths: int, assists: int) -> str | float:
    """Handles KDA with no deaths"""
    if not deaths:
        return "PERF 👑"
    else:
        return round((kills + assists) / deaths, 1)


def calc_participant_percent(participant_stat: int | float, team_stat: int | float) -> str:
    """Compares a participants stats to the team's as a whole"""
    return f"{round((participant_stat / team_stat) * 100)}%"


def calc_carry_factor(participant_stat: cass.core.match.ParticipantStats) -> int:
    """Josh's experiemental carry score"""
    carry_factor: int = 0

    # Earn CF
    carry_factor += participant_stat.kills * 2
    carry_factor += participant_stat.assists
    carry_factor += participant_stat.gold_earned // 100
    carry_factor += participant_stat.turret_takedowns
    carry_factor += participant_stat.inhibitor_takedowns

    # Lose CF
    carry_factor -= participant_stat.deaths * 3
    carry_factor -= participant_stat.turrets_lost // 3  # Makes you responsible for 1/3 of turrets
    carry_factor -= participant_stat.inhibitors_lost // 3  # ^... inhibs

    return carry_factor
