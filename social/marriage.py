"""婚姻结拜"""
import calendar
from dataclasses import dataclass, field
from datetime import date

MARRIAGE_BONUS = {"atk": 10, "def": 10}

@dataclass
class Player:
    pid: str
    married: bool = False
    spouse: str = None
    bonus: dict = field(default_factory=dict)
    property_before: int = 0
    property_after: int = 0

class MarriageSystem:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.ceremony_slots: dict[str, tuple] = {}

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
        if p1 not in self.players or p2 not in self.players:
            return False
        if self.players[p1].spouse != p2 or self.players[p2].spouse != p1:
            return False
        self.players[p1].married = False
        self.players[p1].spouse = None
        self.players[p1].bonus.clear()
        self.players[p2].married = False
        self.players[p2].spouse = None
        self.players[p2].bonus.clear()
        return True

    def check_anniversary(self, marry_date: date, today: date) -> bool:
        if marry_date.month == 2 and marry_date.day == 29:
            if not calendar.isleap(today.year):
                return today.month == 2 and today.day == 28
        return marry_date.month == today.month and marry_date.day == today.day

    def split_property(self, p1: str, p2: str) -> tuple:
        player1 = self.players[p1]
        player2 = self.players[p2]
        marital = player1.property_after + player2.property_after
        p1_share = player1.property_before + marital // 2
        p2_share = player2.property_before + marital - marital // 2
        return (p1_share, p2_share)

    def start_wedding_ceremony(self, p1: str, p2: str, venue: str) -> bool:
        if venue in self.ceremony_slots:
            return False
        self.ceremony_slots[venue] = (p1, p2)
        return True

    def end_wedding_ceremony(self, venue: str) -> bool:
        if venue not in self.ceremony_slots:
            return False
        del self.ceremony_slots[venue]
        return True
