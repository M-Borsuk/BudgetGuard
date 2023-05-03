from conftest import SparkETLTestCase


class TestDummy(SparkETLTestCase):
    def test_base(self):
        assert 1 == 1
