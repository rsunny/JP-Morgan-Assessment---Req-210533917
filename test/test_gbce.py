from datetime import datetime

import pytest

from src.constants import IndicatorConst
from src.gbce import GBCE


@pytest.fixture
def gbce(stock_tea, stock_pop):
    gbce = GBCE()
    gbce.add_stock(stock_tea)
    gbce.add_stock(stock_pop)
    return gbce


def test_add_stock(gbce, stock_gin):
    gbce.add_stock(stock_gin)
    assert gbce.get_stock("GIN") == stock_gin


def test_add_stock_duplicate_fails(gbce, stock_gin):
    gbce.add_stock(stock_gin)
    try:
        gbce.add_stock(stock_gin)
        assert False
    except ValueError:
        assert True


def test_load_stocks():
    gbce = GBCE()
    gbce.load_stocks()
    assert gbce.get_all_stocks().keys() == {"TEA", "POP", "ALE", "GIN", "JOE"}


def test_gbce_all_share_index(gbce, stock_tea, stock_pop):
    stock_tea.record_trade(
        int(datetime.now().timestamp()), 100, IndicatorConst.BUY, 105
    )
    stock_pop.record_trade(
        int(datetime.now().timestamp()), 100, IndicatorConst.BUY, 110
    )
    expected = (105 * 110) ** 0.5
    assert gbce.gbce_all_share_index() == expected
