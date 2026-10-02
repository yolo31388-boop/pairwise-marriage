"""婚姻结拜系统"""
from calendar import isleap
from dataclasses import dataclass, field
from datetime import date

MARRIAGE_BONUS = {"atk": 10, "def": 10}

@dataclass
class Player:
    pid: str
    married: bool = False
    spouse: str | None = None
    bonus: dict = field(default_factory=dict)
    property_before: int = 0   # 婚前财产，归个人所有
    property_after: int = 0    # 婚后共同财产

class MarriageSystem:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.ceremony_slots: dict[str, tuple[str, str]] = {}

    def marry(self, p1: str, p2: str) -> bool:
        if p1 == p2:
            return False
        if p1 not in self.players:
            self.players[p1] = Player(p1)
        if p2 not in self.players:
            self.players[p2] = Player(p2)
        if self.players[p1].married or self.players[p2].married:
            return False
        self.players[p1].married = True
        self.players[p1].spouse = p2
        self.players[p2].married = True
        self.players[p2].spouse = p1
        self.apply_bonus(p1)
        self.apply_bonus(p2)
        return True

    def apply_bonus(self, pid: str) -> dict:
        player = self.players.get(pid)
        if player is None or not player.married:
            return {}
        player.bonus.update(MARRIAGE_BONUS)
        return dict(player.bonus)

    def divorce(self, p1: str, p2: str) -> bool:
        player1 = self.players.get(p1)
        player2 = self.players.get(p2)
        if (player1 is None or player2 is None
                or player1.spouse != p2 or player2.spouse != p1):
            return False
        for key in MARRIAGE_BONUS:
            player1.bonus.pop(key, None)
            player2.bonus.pop(key, None)
        player1.married = False
        player1.spouse = None
        player2.married = False
        player2.spouse = None
        return True

    def check_anniversary(self, marry_date: date, today: date) -> bool:
        if (marry_date.month, marry_date.day) == (2, 29):
            if isleap(today.year):
                return (today.month, today.day) == (2, 29)
            return (today.month, today.day) == (2, 28)
        return marry_date.month == today.month and marry_date.day == today.day

    def split_property(self, p1: str, p2: str) -> tuple:
        player1 = self.players[p1]
        player2 = self.players[p2]
        half, remainder = divmod(
            player1.property_after + player2.property_after, 2
        )
        return (
            player1.property_before + half + remainder,
            player2.property_before + half,
        )

    def start_wedding_ceremony(self, venue: str, p1: str, p2: str) -> bool:
        couple = (p1, p2)
        occupied_by = self.ceremony_slots.get(venue)
        if occupied_by is not None and occupied_by != couple:
            return False
        self.ceremony_slots[venue] = couple
        return True

    def end_wedding_ceremony(self, venue: str) -> bool:
        return self.ceremony_slots.pop(venue, None) is not None
