from dataclasses import dataclass


@dataclass
class TradeIntent:
    symbol: str
    side: str
    size: float
