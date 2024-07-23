from datetime import datetime
from heapq import heappop, heappush
from typing import List, Optional

from src.constants import IndicatorType, StockType, StockTypeConst
from src.trade import Trade


class Stock:
    def __init__(
        self,
        symbol: str,
        stock_type: StockType,
        last_dividend: float,
        fixed_dividend: Optional[float],
        par_value: float,
    ) -> None:
        self.__symbol = symbol
        self.__stock_type = stock_type
        self.__last_dividend = last_dividend
        self.__fixed_dividend = fixed_dividend
        self.__par_value = par_value
        self.__trades: List[Trade] = []
        # min_heap on (timestamp, trade_index), earliest trade on top
        self.__trades_heap: List[tuple[str, int]] = []
        self.__total_quantity = 0
        self.__total_volume = 0

    def get_symbol(self) -> str:
        return self.__symbol

    def get_trades(self) -> list[Trade]:
        return self.__trades

    def dividend_yield(self, price: float) -> float:
        if price == 0:
            return 0
        if self.__stock_type == StockTypeConst.COMMON:
            return self.__last_dividend / price
        elif self.__stock_type == StockTypeConst.PREFERRED:
            return (self.__fixed_dividend * self.__par_value) / price

    def pe_ratio(self, price: float) -> float:
        # Assuming that the dividend is the dividend yield * price
        dividend = self.dividend_yield(price) * price
        if dividend == 0:
            return 0
        return price / dividend

    def record_trade(
        self, timestamp: str, quantity: int, indicator: IndicatorType, price: float
    ):
        # Assuming timestamp is an UNIX epoch timestamp
        # Also assuming that the timestamp is not always increasing, hence the need for a min_heap
        self.__trades.append(
            Trade(
                timestamp=timestamp, quantity=quantity, indicator=indicator, price=price
            )
        )
        self.__total_quantity += quantity
        self.__total_volume += price * quantity
        heappush(self.__trades_heap, (timestamp, len(self.__trades) - 1))

    def volume_weighted_stock_price(self) -> float:
        five_minutes_ago = int(datetime.now().timestamp()) - 300
        print(self.__trades_heap, five_minutes_ago)
        for trade in self.__trades:
            print(
                trade.timestamp,
                trade.timestamp < five_minutes_ago,
                trade.quantity,
                trade.price,
            )
        # Remove trades older than 5 minutes
        while self.__trades_heap and self.__trades_heap[0][0] < five_minutes_ago:
            _, trade_index = heappop(self.__trades_heap)
            trade = self.__trades[trade_index]
            self.__total_quantity -= trade.quantity
            self.__total_volume -= trade.price * trade.quantity

        return (
            0
            if self.__total_quantity == 0
            else self.__total_volume / self.__total_quantity
        )
