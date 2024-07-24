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

        # Min-heap to maintain trades with timestamps
        # Heap stores tuples of (timestamp, trade_index) with the earliest trade on top
        self.__trades_heap: List[tuple[int, int]] = []
        self.__total_quantity = 0
        self.__total_volume = 0

    def get_symbol(self) -> str:
        return self.__symbol

    def get_trades(self) -> List[Trade]:
        return self.__trades

    def dividend_yield(self, price: float) -> float:
        if price == 0:
            return 0
        if self.__stock_type == StockTypeConst.COMMON:
            return self.__last_dividend / price
        elif self.__stock_type == StockTypeConst.PREFERRED:
            return (self.__fixed_dividend * self.__par_value) / price

    def pe_ratio(self, price: float) -> float:
        # Assuming that the dividend is the dividend_yield * price
        dividend = self.dividend_yield(price) * price
        if dividend == 0:
            return 0
        return price / dividend

    def record_trade(
        self, timestamp: int, quantity: int, indicator: IndicatorType, price: float
    ):
        """
        Record a trade with the given timestamp, quantity, indicator, and price.
        Trades are stored in a min-heap to efficiently manage the removal of old trades.

        Parameters:
        - timestamp (int): The UNIX epoch timestamp of the trade.
        - quantity (int): The quantity of stocks traded.
        - indicator (IndicatorType): The trade indicator (buy or sell).
        - price (float): The price at which the trade was executed.
        """
        # Append the trade to the trades list
        self.__trades.append(
            Trade(
                timestamp=timestamp, quantity=quantity, indicator=indicator, price=price
            )
        )
        # Update total quantity and volume
        self.__total_quantity += quantity
        self.__total_volume += price * quantity
        # Push the trade onto the heap
        heappush(self.__trades_heap, (timestamp, len(self.__trades) - 1))

    def volume_weighted_stock_price(self) -> float:
        """
        Calculate the volume weighted stock price based on trades in the last 5 minutes.

        Returns:
        - float: The volume weighted stock price.
        """
        # Calculate the timestamp for five minutes ago
        five_minutes_ago = int(datetime.now().timestamp()) - 300
        # Remove trades older than 5 minutes and adjust total quantity and volume
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
