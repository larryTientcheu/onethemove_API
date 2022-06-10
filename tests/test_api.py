import pytest

def sum(a,b):
    return a+b

class TestUsers:
    def test_sum(self):
        assert sum(4,3) == 8, "Should be 7"
