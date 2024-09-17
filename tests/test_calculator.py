from __future__ import annotations

import pytest


def test_add(valid_calc_input):
    assert valid_calc_input.add() == 5


def test_subtract(valid_calc_input):
    assert valid_calc_input.subtract() == -1


def test_multiply(valid_calc_input):
    assert valid_calc_input.multiply() == 6


def test_divide(valid_calc_input):
    assert valid_calc_input.divide() == 0.6666666666666666


def test_divide_by_zero(valid_calc_input):
    valid_calc_input.b = 0
    with pytest.raises(ZeroDivisionError):
        valid_calc_input.divide()
