import pytest
from add_wrapper import Add

def test_add():
    assert Add(1,-1) == 0
    assert Add(1, 1) == 2
    assert Add(-1,-1) == -2
    assert Add(0,0) == 0
    assert Add(0,10) != 0