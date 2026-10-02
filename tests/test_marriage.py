"""婚姻结拜 - 测试"""
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
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        ms.players["b"] = Player("b", married=True, spouse="x")
        assert ms.marry("a", "b") == False
        assert ms.players["a"].married == False

    def test_cannot_marry_self(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        assert ms.marry("a", "a") == False
        assert ms.players["a"].married == False


class TestBonusPersistence:
    def test_bonus_applied_to_player_data(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a")
        ms.players["b"] = Player("b")
        ms.marry("a", "b")
        ms.apply_bonus("a")
        assert "atk" in ms.players["a"].bonus

    def test_bonus_survives_relogin(self):
        ms = MarriageSystem()
        ms.marry("a", "b")
        saved = dict(ms.players["a"].bonus)
        ms2 = MarriageSystem()
        ms2.players["a"] = Player("a", married=True, spouse="b", bonus=saved)
        assert ms2.players["a"].bonus["atk"] == 10
        assert ms2.apply_bonus("a")["def"] == 10


class TestDivorceRemovesBonus:
    def test_divorce_removes_marriage_bonus(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", married=True, spouse="b", bonus={"atk": 10})
        ms.players["b"] = Player("b", married=True, spouse="a")
        ms.divorce("a", "b")
        assert ms.players["a"].bonus == {}

    def test_divorce_removes_bonus_for_both_parties(self):
        ms = MarriageSystem()
        ms.marry("a", "b")
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

    def test_leap_day_anniversary_in_leap_year(self):
        ms = MarriageSystem()
        marry = date(2024, 2, 29)
        assert ms.check_anniversary(marry, date(2028, 2, 29)) == True
        assert ms.check_anniversary(marry, date(2025, 3, 1)) == False

    def test_normal_anniversary_unchanged(self):
        ms = MarriageSystem()
        marry = date(2023, 5, 20)
        assert ms.check_anniversary(marry, date(2025, 5, 20)) == True
        assert ms.check_anniversary(marry, date(2025, 5, 21)) == False


class TestPropertySplit:
    def test_premarital_property_not_split(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", property_before=1000)
        ms.players["b"] = Player("b", property_before=500)
        p1_share, p2_share = ms.split_property("a", "b")
        assert p1_share == 1000

    def test_marital_property_split_evenly(self):
        ms = MarriageSystem()
        ms.players["a"] = Player("a", property_before=1000, property_after=300)
        ms.players["b"] = Player("b", property_before=500, property_after=100)
        p1_share, p2_share = ms.split_property("a", "b")
        assert p1_share == 1200
        assert p2_share == 700


class TestCeremonyVenue:
    def test_venue_cannot_be_double_booked(self):
        ms = MarriageSystem()
        assert ms.start_wedding_ceremony("hall1", "a", "b") == True
        assert ms.start_wedding_ceremony("hall1", "c", "d") == False
        assert ms.end_wedding_ceremony("hall1") == True
        assert ms.start_wedding_ceremony("hall1", "c", "d") == True
