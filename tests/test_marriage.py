"""婚姻结拜 - 红态测试"""
import pytest, sys, os
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from social.marriage import MarriageSystem, Player

class TestNoBigamy:
    def test_cannot_marry_if_already_married(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", married=True, spouse="x")
        ms.players["b"] = Player("b")
        assert ms.marry("a", "b") == False

class TestBonusPersistence:
    def test_bonus_applied_to_player_data(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        ms.players["b"] = Player("b")
        ms.marry("a", "b")
        ms.apply_bonus("a")
        assert "atk" in ms.players["a"].bonus

class TestDivorceRemovesBonus:
    def test_divorce_removes_marriage_bonus(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", married=True, spouse="b", bonus={"atk": 10})
        ms.players["b"] = Player("b", married=True, spouse="a")
        ms.divorce("a", "b")
        assert ms.players["a"].bonus == {}

class TestLeapYearAnniversary:
    def test_leap_day_anniversary_triggers_on_feb28(self):
        ms = MarriageSystem()
        marry = date(2024, 2, 29)
        today = date(2025, 2, 28)
        assert ms.check_anniversary(marry, today) == True

class TestPropertySplit:
    def test_premarital_property_not_split(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", property_before=1000)
        ms.players["b"] = Player("b", property_before=500)
        p1_share, p2_share = ms.split_property("a", "b")
        assert p1_share == 1000
