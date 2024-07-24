from typing import Literal


class StockTypeConst:
    COMMON = "Common"
    PREFERRED = "Preferred"


class IndicatorConst:
    BUY = "buy"
    SELL = "sell"


# Type alias for StockType using Literal to restrict to defined stock types
StockType = Literal["Common", "Preferred"]

# Type alias for IndicatorType using Literal to restrict to defined indicators
IndicatorType = Literal["buy", "sell"]
