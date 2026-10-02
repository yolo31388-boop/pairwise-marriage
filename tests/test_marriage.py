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

    def test_cannot_marry_self(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        assert ms.marry("a", "a") == False
        assert ms.players["a"].married == False
        assert ms.players["a"].spouse is None

class TestBonusPersistence:
    def test_bonus_applied_to_player_data(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        ms.players["b"] = Player("b")
        ms.marry("a", "b")
        ms.apply_bonus("a")
        assert "atk" in ms.players["a"].bonus

    def test_bonus_reapplied_after_relogin(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        ms.players["b"] = Player("b")
        ms.marry("a", "b")
        ms.apply_bonus("a")
        ms.apply_bonus("a")
        assert ms.players["a"].bonus == {"atk": 10, "def": 10}

class TestDivorceRemovesBonus:
    def test_divorce_removes_marriage_bonus(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", married=True, spouse="b", bonus={"atk": 10})
        ms.players["b"] = Player("b", married=True, spouse="a")
        ms.divorce("a", "b")
        assert ms.players["a"].bonus == {}

    def test_divorce_removes_bonus_from_both_spouses(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", married=True, spouse="b", bonus={"atk": 10, "def": 10})
        ms.players["b"] = Player("b", married=True, spouse="a", bonus={"atk": 10, "def": 10})
        assert ms.divorce("a", "b") == True
        assert ms.players["a"].bonus == {}
        assert ms.players["b"].bonus == {}
        assert ms.players["a"].married == False
        assert ms.players["b"].married == False

class TestLeapYearAnniversary:
    def test_leap_day_anniversary_triggers_on_feb28(self):
        ms = MarriageSystem()
        marry = date(2024, 2, 29)
        today = date(2025, 2, 28)
        assert ms.check_anniversary(marry, today) == True

    def test_leap_day_anniversary_in_actual_leap_year(self):
        ms = MarriageSystem()
        marry = date(2024, 2, 29)
        assert ms.check_anniversary(marry, date(2028, 2, 29)) == True
        assert ms.check_anniversary(marry, date(2025, 2, 27)) == False
        assert ms.check_anniversary(marry, date(2025, 3, 1)) == False

class TestPropertySplit:
    def test_premarital_property_not_split(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", property_before=1000)
        ms.players["b"] = Player("b", property_before=500)
        p1_share, p2_share = ms.split_property("a", "b")
        assert p1_share == 1000

    def test_marital_property_split_equally(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", property_before=1000, property_after=400)
        ms.players["b"] = Player("b", property_before=500, property_after=200)
        p1_share, p2_share = ms.split_property("a", "b")
        assert p1_share == 1300
        assert p2_share == 800

class TestWeddingVenue:
    def test_occupied_venue_rejected(self):
        ms = MarriageSystem()
        assert ms.start_wedding_ceremony("a", "b", "hall1") == True
        assert ms.start_wedding_ceremony("c", "d", "hall1") == False

    def test_venue_available_after_ceremony_ends(self):
        ms = MarriageSystem()
        ms.start_wedding_ceremony("a", "b", "hall1")
        assert ms.end_wedding_ceremony("hall1") == True
        assert ms.start_wedding_ceremony("c", "d", "hall1") == True
