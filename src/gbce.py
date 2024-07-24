from math import prod

from src.data.stocks import stocks_data
from src.stock import Stock


class GBCE:
    def __init__(self) -> None:
        """
        Initialize a new instance of the GBCE class.
        This class is responsible for managing stocks and calculating the GBCE All Share Index.
        """
        self.__stocks: dict[str, Stock] = {}

    def add_stock(self, stock: Stock):
        """
        Add a new stock to the GBCE.

        Parameters:
        - stock (Stock): The stock to be added.
        """
        symbol = stock.get_symbol()
        if symbol in self.__stocks:
            raise ValueError(f"Stock with symbol {symbol} already exists")
        self.__stocks[symbol] = stock

    def load_stocks(self):
        """
        Load stocks from the stocks_data list.
        """
        for stock_data in stocks_data:
            stock = Stock(
                symbol=stock_data["symbol"],
                stock_type=stock_data["type"],
                last_dividend=stock_data["last_dividend"],
                fixed_dividend=stock_data["fixed_dividend"],
                par_value=stock_data["par_value"],
            )
            if stock.get_symbol() not in self.__stocks:
                self.add_stock(stock)

    def get_stock(self, symbol: str) -> Stock:
        """
        Retrieve a stock by its symbol.

        Parameters:
        - symbol (str): The symbol of the stock to retrieve.

        Returns:
        - Stock: The stock corresponding to the provided symbol.

        Raises:
        - KeyError: If the stock with the specified symbol is not found.
        """
        if symbol not in self.__stocks:
            raise KeyError(f"Stock with symbol {symbol} not found")
        return self.__stocks[symbol]

    def get_all_stocks(self) -> dict[str, Stock]:
        """
        Retrieve all stocks.

        Returns:
        - dict[str, Stock]: A dictionary containing all stocks, with the symbol as the key.
        """
        return self.__stocks

    def gbce_all_share_index(self) -> float:
        """
        Calculate the GBCE All Share Index.
        The GBCE All Share Index is calculated using the geometric mean of the volume weighted stock prices for all stocks.

        Returns:
        - float: The GBCE All Share Index.
        """
        # Calculate the volume weighted stock price for each stock and store values greater than 0
        vwsp_values = [
            stock.volume_weighted_stock_price()
            for stock in self.__stocks.values()
            if stock.volume_weighted_stock_price() > 0
        ]
        if not vwsp_values:
            return 0

        # Calculate the geometric mean of the volume weighted stock prices
        # Note: Using prod(vwsp_values) ** (1 / len(vwsp_values) lead to overflow issues
        # hence changed to the following to avoid that
        return prod([value ** (1 / len(vwsp_values)) for value in vwsp_values])
