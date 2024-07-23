from datetime import datetime

from src.constants import IndicatorConst


def test_dividend_yield_common(stock_tea):
    assert stock_tea.dividend_yield(100) == 0


def test_dividend_yield_preferred(stock_gin):
    assert stock_gin.dividend_yield(100) == 0.02


def test_pe_ratio(stock_pop):
    assert stock_pop.pe_ratio(100) == 12.5


def test_record_trade(stock_pop):
    stock_pop.record_trade(
        int(datetime.now().timestamp()), 100, IndicatorConst.BUY, 105
    )
    assert len(stock_pop.get_trades()) == 1


def test_volume_weighted_stock_price(stock_tea, example_trades):
    for trade in example_trades:
        stock_tea.record_trade(
            trade.timestamp, trade.quantity, trade.indicator, trade.price
        )
    expected = (105 * 100 + 107 * 200) / (100 + 200)
    assert stock_tea.volume_weighted_stock_price() == expected
