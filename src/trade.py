from src.constants import IndicatorType


class Trade:
    def __init__(
        self, timestamp: str, quantity: int, indicator: IndicatorType, price: float
    ) -> None:
        self.timestamp = timestamp
        self.quantity = quantity
        self.indicator = indicator
        self.price = price
