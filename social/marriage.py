"""婚姻结拜 - 含5个bug"""
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Player:
    pid: str
    married: bool = False
    spouse: str = None
    bonus: dict = field(default_factory=dict)
    property_before: int = 0

class MarriageSystem:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.ceremony_slots: dict[str, str] = {}  # bug6: 场地占用

    def marry(self, p1: str, p2: str) -> bool:
        # bug1: 不检查双方婚姻状态
        if p1 not in self.players:
            self.players[p1] = Player(p1)
        if p2 not in self.players:
            self.players[p2] = Player(p2)
        self.players[p1].married = True
        self.players[p1].spouse = p2
        self.players[p2].married = True
        self.players[p2].spouse = p1
        return True

    def apply_bonus(self, pid: str) -> dict:
        # bug2: 不持久化
        return {"atk": 10, "def": 10}

    def divorce(self, p1: str, p2: str) -> bool:
        # bug3: 不移除属性加成
        if p1 in self.players:
            self.players[p1].married = False
            self.players[p1].spouse = None
        if p2 in self.players:
            self.players[p2].married = False
            self.players[p2].spouse = None
        return True

    def check_anniversary(self, marry_date: date, today: date) -> bool:
        # bug4: 闰年2月29日
        return marry_date.month == today.month and marry_date.day == today.day

    def split_property(self, p1: str, p2: str) -> tuple:
        # bug5: 不区分婚前财产
        total = self.players[p1].property_before + self.players[p2].property_before
        return (total // 2, total // 2)
