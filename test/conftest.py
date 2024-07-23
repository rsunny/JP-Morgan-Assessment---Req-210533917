from datetime import datetime

import pytest

from src.constants import IndicatorConst, StockTypeConst
from src.stock import Stock
from src.trade import Trade


@pytest.fixture
def stock_tea():
    return Stock(
        symbol="TEA",
        stock_type=StockTypeConst.COMMON,
        last_dividend=0,
        fixed_dividend=None,
        par_value=100,
    )


@pytest.fixture
def stock_pop():
    return Stock(
        symbol="POP",
        stock_type=StockTypeConst.COMMON,
        last_dividend=8,
        fixed_dividend=None,
        par_value=100,
    )


@pytest.fixture
def stock_gin():
    return Stock(
        symbol="GIN",
        stock_type=StockTypeConst.PREFERRED,
        last_dividend=8,
        fixed_dividend=0.02,
        par_value=100,
    )


@pytest.fixture
def example_trades():
    return [
        Trade(
            timestamp=int(datetime.now().timestamp()) - 200,
            quantity=100,
            indicator=IndicatorConst.BUY,
            price=105,
        ),
        Trade(
            timestamp=int(datetime.now().timestamp()) - 100,
            quantity=200,
            indicator=IndicatorConst.SELL,
            price=107,
        ),
        Trade(
            timestamp=int(datetime.now().timestamp()) - 600,
            quantity=150,
            indicator=IndicatorConst.BUY,
            price=102,
        ),
    ]
