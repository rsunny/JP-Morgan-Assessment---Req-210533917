from math import prod

from src.stock import Stock


class GBCE:
    def __init__(self) -> None:
        self.__stocks: dict[str, Stock] = {}

    def add_stock(self, stock: Stock):
        symbol = stock.get_symbol()
        self.__stocks[symbol] = stock

    def get_stock(self, symbol: str) -> Stock:
        if symbol not in self.__stocks:
            raise KeyError(f"Stock with symbol {symbol} not found")
        return self.__stocks[symbol]

    def gbce_all_share_index(self) -> float:
        vwsp_values = [
            stock.volume_weighted_stock_price()
            for stock in self.__stocks.values()
            if stock.volume_weighted_stock_price() > 0
        ]
        if not vwsp_values:
            return 0

        return prod([value ** (1 / len(vwsp_values)) for value in vwsp_values])
