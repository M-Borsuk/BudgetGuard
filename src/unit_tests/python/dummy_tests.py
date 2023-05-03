from src.main.budget_guard.base import NAME
from conftest import SparkETLTestCase


class TestDummy(SparkETLTestCase):
    def test_base():
        assert NAME == "budgetguard"
