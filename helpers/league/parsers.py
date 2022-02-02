from typing import Iterable

import cassiopeia as cass
from helpers.league.calculators import calc_kda, calc_participant_percent
from helpers.league.format_stat import format_stat as fstat


class LastGameParser:
    """Tidy's up the stats of given summoner's last game"""

    def __init__(self, summoner: cass.Summoner) -> None:
        self.summoner_name = summoner

        # Cass Objects / QoL Variables
        self.last_match: cass.Match = summoner.match_history[0]
        self.participant: cass.core.match.Participant = self.last_match.participants[summoner]  # type: ignore
        self.participant_stats: cass.core.match.ParticipantStats = self.participant.stats
        self.match_timeline: cass.Match.timeline = self.participant.timeline
        self.participant_team: cass.core.match.Team = self.participant.team
        self.match_outcome: bool = self.participant_stats.win
        self.match_queue_type = self.last_match.queue
        self.match_end_time: int = self.last_match.creation.shift(seconds=self.last_match.duration.seconds)
        self.participant_cs: int = (
            self.participant_stats.total_minions_killed + self.participant_stats.neutral_minions_killed
        )
        self.participant_cs_per_min: int = round(
            self.participant_cs / (self.last_match.duration.seconds / 60), 1
        )

        # Spaghetti time! 🍝
        self.team_stats = TeamStatParser(self.participant_team)

    def cs_per_min_stats(self) -> list[str]:
        return [fstat(self.participant_cs, "CS"), fstat(self.participant_cs_per_min, "CS/Min")]

    def kda_stats(self) -> list[str]:
        return [
            fstat(
                stat=f"{self.participant_stats.kills}/{self.participant_stats.deaths}/{self.participant_stats.assists}",
                description="K/D/A",
            ),
            fstat(
                stat=calc_kda(
                    self.participant_stats.kills,
                    self.participant_stats.deaths,
                    self.participant_stats.assists,
                ),
                description="K+A / D",
            ),
        ]

    def damage_dealt_stats(self) -> list[str]:
        return [
            fstat(
                calc_participant_percent(
                    self.participant_stats.total_damage_dealt_to_champions,
                    self.team_stats.total_damage_to_champions,
                ),
                "vs champs 🎯",
            ),
            fstat(
                calc_participant_percent(
                    self.participant_stats.damage_dealt_to_objectives,
                    self.team_stats.total_damage_to_objectives,
                ),
                "vs objectives 🛡",
            ),
        ]


class TeamStatParser:
    """Mostly adds-up the entire team's worth of a particular stat"""

    def __init__(self, team: cass.core.match.Team) -> None:
        self.team = team
        self.total_damage_to_champions: int = 0
        self.total_damage_to_objectives: int = 0
        self.total_heals_on_teammates: int = 0

        for participant in self.team.participants:
            participant: cass.core.match.Participant
            participant_stats: cass.core.match.ParticipantStats = participant.stats
            self.total_damage_to_champions += participant_stats.total_damage_dealt_to_champions
            self.total_damage_to_objectives += participant_stats.damage_dealt_to_objectives
            self.total_heals_on_teammates += participant_stats.total_heals_on_teammates
