from django.test import TestCase
import pandas as pd
import os

# Create your tests here.
from analysis.core.service.fund import fetch_fund_data
from analysis.core.service.pattern import get_bb_data


def test_path():
    print(os.getcwd())
    print(__file__)
    print(os.path.dirname(__file__))
    print(os.stat("../core/data/raw"))


def test_fetch_fund_data():
    fetch_fund_data(["000220"])
