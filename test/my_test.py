
import pytest
import datetime as dt
import pandas as pd
import quandl
import os
from dotenv import load_dotenv
from yahoo_fin.stock_info import get_analysts_info, get_data
load_dotenv()

from app.stock-analysis import sort_growth

from app.stock-analysis import min_growth

from app.stock-analysis import max_growth

test_list = ["2.5%", "1.0%", "9.5%"]
def test_sort_growth():
    result = sort_growth(test_list)
    assert result == ['1.0 %', '2.5 %', '9.5 %']

test_sorted_list = ['1.0 %', '2.5 %', '9.5 %']

def test_min_growth():
    result = min_growth(test_sorted_list)
    assert result == '1.0 %'


