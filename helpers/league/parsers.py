import queue
from dataclasses import dataclass
from random import choice, shuffle

import cassiopeia as cass
from helpers.league.calculators import calc_kda, calc_participant_percent
from helpers.league.format_stat import format_stat as fstat


class LastGameParser:
    """Tidy's up the stats of given summoner's last game"""

    def __init__(self, summoner: cass.Summoner) -> None:
        self.summoner = summoner
        self.summoner_name = summoner.name

        # Cass Objects / QoL Variables
        self.last_match: cass.Match = self.summoner.match_history[0]

        self.participant: cass.core.match.Participant = self.last_match.participants[self.summoner]  # type: ignore
        self.participant_enemy_team: cass.core.match.Team = self.participant.enemy_team
        self.participant_stats: cass.core.match.ParticipantStats = self.participant.stats
        self.participant_team: cass.core.match.Team = self.participant.team
        self.participant_cs: int = self.participant_stats.total_minions_killed + self.participant_stats.neutral_minions_killed
        self.participant_cs_per_min: int = round(self.participant_cs / (self.last_match.duration.seconds / 60), 1)

        self.match_end_time: int = self.last_match.creation.shift(seconds=self.last_match.duration.seconds)
        self.match_timeline: cass.Match.timeline = self.participant.timeline
        self.match_outcome: bool = self.participant_stats.win
        self.match_queue_type = self.last_match.queue

        # Spaghetti time! 🍝
        self.team_stats = TeamStatParser(self.participant_team)
        self.enemy_team_stats = TeamStatParser(self.participant_enemy_team)

    @property
    def teammates(self) -> list[str]:
        return [teammate.summoner.name for teammate in self.participant_team.participants if teammate.summoner != self.summoner]

    @property
    def cs_stats(self) -> list[str]:
        return [fstat(self.participant_cs, f"CS ({self.participant_cs_per_min}/min)")]

    @property
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

    @property
    def carry_stats(self) -> list:
        return [
            fstat(
                calc_participant_percent(
                    self.participant_stats.total_damage_dealt_to_champions,
                    self.team_stats.total_damage_to_champions,
                ),
                "team dmg vs champs",
            ),
            fstat(
                calc_participant_percent(
                    self.participant_stats.damage_dealt_to_objectives,
                    self.team_stats.total_damage_to_objectives,
                ),
                "team dmg vs objectives",
            ),
            fstat(
                calc_participant_percent(
                    self.participant_stats.gold_earned,
                    self.team_stats.gold_earned,
                ),
                "team gold",
            ),
            fstat(
                calc_participant_percent(
                    self.participant_stats.kills + self.participant_stats.assists,
                    self.team_stats.kills,
                ),
                "kill partication",
            ),
            fstat(
                calc_participant_percent(
                    self.participant_stats.deaths,
                    self.team_stats.deaths,
                ),
                "death partication",
            ),
            # fstat(f"{round(self.participant_stats.longest_time_spent_living / 60, 1)}m", "longest time alive"), #? Disabled, unexpected behavior. Keeping for reference
            *self.multi_kill_stats,
        ]

    @property
    def multi_kill_stats(self) -> list[str]:
        """Returns a list of all the multikills (if any)"""

        @dataclass
        class MultiKill:
            count: int
            title: str

        multi_kills: list[MultiKill] = [
            MultiKill(self.participant_stats.double_kills, "double kill(s)"),
            MultiKill(self.participant_stats.triple_kills, "triple kill(s)"),
            MultiKill(self.participant_stats.quadra_kills, "quadra kill(s)"),
            MultiKill(self.participant_stats.penta_kills, "penta kill(s)"),
        ]
        return [fstat(multi_kill.count, multi_kill.title) for multi_kill in multi_kills if multi_kill.count > 0]

    @property
    def vision_stats(self) -> list[str]:
        return [
            fstat(self.participant_stats.vision_score, "vision score"),
            fstat(self.participant_stats.vision_wards_bought, "pink(s) bought"),
            fstat(self.participant_stats.wards_killed, "wards killed"),
        ]

    @property
    def game_stats(self) -> list[str]:
        return [fstat(self.team_stats.kills, "team kills"), fstat(self.enemy_team_stats.kills, "enemy kills")]

    @property
    def final_build(self) -> list[str]:
        return [item.name for item in self.participant_stats.items if item is not None]

    @property
    def summoner_spells(self) -> list[str]:
        return [self.participant.summoner_spell_d.name, self.participant.summoner_spell_f.name]

    @property
    def spells_used(self) -> list[str]:
        return [
            fstat(self.participant_stats.spell_1_casts, "Qs"),
            fstat(self.participant_stats.spell_2_casts, "Ws"),
            fstat(self.participant_stats.spell_3_casts, "Es"),
            fstat(self.participant_stats.spell_4_casts, "Rs"),
        ]


class TeamStatParser:
    """Mostly adds-up the entire team's worth of a particular stat"""

    def __init__(self, team: cass.core.match.Team) -> None:
        self.team = team
        self.total_damage_to_champions: int = 0
        self.total_damage_to_objectives: int = 0
        self.total_heals_on_teammates: int = 0
        self.kills: int = 0
        self.deaths: int = 0
        self.assists: int = 0
        self.gold_earned: int = 0

        for participant in self.team.participants:
            participant: cass.core.match.Participant
            participant_stats: cass.core.match.ParticipantStats = participant.stats
            self.total_damage_to_champions += participant_stats.total_damage_dealt_to_champions
            self.total_damage_to_objectives += participant_stats.damage_dealt_to_objectives
            self.total_heals_on_teammates += participant_stats.total_heals_on_teammates
            self.kills += participant_stats.kills
            self.deaths += participant_stats.deaths
            self.assists += participant_stats.assists
            self.gold_earned += participant_stats.gold_earned


class LastTeamParser:
    """Lmao"""

    def __init__(self, summoner: cass.Summoner) -> None:
        self.summoner = summoner
        self.last_match: cass.Match = self.summoner.match_history[0]
        self.participant: cass.core.match.Participant = self.last_match.participants[self.summoner]  # type: ignore
        self.participant_team: cass.core.match.Team = self.participant.team
        self.participant_cs: int = self.participant.stats.total_minions_killed + self.participant.stats.neutral_minions_killed
        self.participant_cs_per_min: int = round(self.participant_cs / (self.last_match.duration.seconds / 60), 1)
        self.last_teammates: list[cass.core.match.Participant] = [teammate for teammate in self.participant_team.participants]

    def make_troll_stats(self, teammate: cass.core.match.ParticipantStats) -> list[str]:
        """Returns a list of Josh's custom stat badges. 'Troll' because they're meant to be lighthearted."""

        @dataclass
        class StatDetail:
            amount: int | float | bool
            badge: str
            min_thresh: int | float | bool

        troll_stats = [
            StatDetail(teammate.deaths + teammate.assists, choice(["FEEDER", "Feedster", "Sus!"]), teammate.kills),
            StatDetail(teammate.total_heals_on_teammates, choice(["Heal Slut"]), 10_000),
            # StatDetail(teammate.total_damage_shielded_on_teammates, "Big shielder 🛡", 5000),
            StatDetail(teammate.nexus_takedowns + teammate.inhibitor_takedowns, "Tower Destroyer", 4),
            StatDetail(self.participant_cs_per_min, f"Farmer Grind", 8),
            StatDetail(teammate.largest_killing_spree, f"Huge killing spree", 8),
            StatDetail(teammate.double_kills, f"Double-Double!", 2),
            StatDetail(teammate.triple_kills, f"Triple-Triple!", 3),
            StatDetail(teammate.quadra_kills, f"Quadra-Quadra!", 4),  # Never gonna happen outside of iron
            StatDetail(teammate.penta_kills, f"Penta-Penta!", 5),  # Not possible, I'm calling it
            StatDetail(teammate.total_damage_dealt_to_champions, f"Damage dealer", 60_000),
            StatDetail(teammate.largest_multi_kill, f"Multikiller", 4),
            StatDetail(teammate.largest_critical_strike, f"Crit strike abuser ", 10_000),
            StatDetail(teammate.time_CCing_others, f"CC Bot", 20),
            StatDetail(teammate.wards_killed, f"Ward Killer", 10),
            StatDetail(teammate.wards_placed, f"Good Vision", 10),
        ]
        return [stat.badge for stat in troll_stats if stat.amount > stat.min_thresh]  # Returns stat badges if count > min_thresh


class SummonerLookup:
    def __init__(self, summoner: cass.Summoner) -> None:
        self.summoner = summoner
        self.ranked_matches: cass.MatchHistory = summoner.match_history(begin_index=0, end_index=20)  # Not working =/
        for match in self.ranked_matches:
            match: cass.Match
            print(match.participants)
