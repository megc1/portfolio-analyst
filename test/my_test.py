import pytest
import datetime as dt
import pandas as pd
import quandl
import os
from dotenv import load_dotenv
import yahoo_fin.stock_info


# from app.stock-analysis import sort_growth

# from app.stock-analysis import min_growth

# from app.stock-analysis import max_growth

def sort_growth(a_list):
    a_list.sort(key = lambda x: float (x[:-1]))
    return a_list

#gets smallest growth percentage
def min_growth(b_list):
    min_value = sort_growth(b_list)[0]
    return min_value

#gets largest growth percentage
def max_growth(c_list):
    max_value = sort_growth(c_list)[-1]
    return max_value

test_list = ["2.5%", "1.0%", "9.5%"]
def test_sort_growth():
    result = sort_growth(test_list)
    assert result == ['1.0 %', '2.5 %', '9.5 %']

test_sorted_list = ['1.0 %', '2.5 %', '9.5 %']

def test_min_growth():
    result = min_growth(test_sorted_list)
    assert result == '1.0 %'


def test_max_growth():
    result = max_growth(test_sorted_list)
    assert result == '9.5 %'
