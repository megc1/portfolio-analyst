import os
import pytest

from app.stock_analysis import sort_growth, min_growth, max_growth, maketable

test_list = ["2.5%", "1.0%", "9.5%"]

def test_sort_growth():
    result = sort_growth(test_list)
    assert result == ['1.0%', '2.5%', '9.5%']

test_sorted_list = ['1.0%', '2.5%', '9.5%']

def test_min_growth():
    result = min_growth(test_sorted_list)
    assert result == '1.0%'

def test_max_growth():
    result = max_growth(test_sorted_list)
    assert result == '9.5%'

test_table = [[' Stock '], ['MSFT'], [' Earnings Estimate '], ['5.11'], [' EPS Trend '], ['5.11'], [' Growth Estimate '], ['7.10%']]
def test_maketable():
    result = maketable(test_table)
    assert 'MSFT' in result
    assert 'Earnings Estimate' in result
    assert 'EPS Trend' in result
    assert '5.11' in result
