from typing import Literal


class StockTypeConst:
    COMMON = "Common"
    PREFERRED = "Preferred"


class IndicatorConst:
    BUY = "buy"
    SELL = "sell"


StockType = Literal["Common", "Preferred"]
IndicatorType = Literal["buy", "sell"]
