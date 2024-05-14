from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field


class Quote(BaseModel):
    field_52_week_high: float | None = Field(default=None, validation_alias="52WeekHigh")
    field_52_week_low: float | None = Field(default=None, validation_alias="52WeekLow")
    ask_price: float | None = Field(default=None, validation_alias="askPrice")
    ask_size: int | None = Field(default=None, validation_alias="askSize")
    bid_price: float | None = Field(default=None, validation_alias="bidPrice")
    bid_size: int | None = Field(default=None, validation_alias="bidSize")
    close_price: float | None = Field(default=None, validation_alias="closePrice")
    high_price: float | None = Field(default=None, validation_alias="highPrice")
    last_price: float | None = Field(default=None, validation_alias="lastPrice")
    last_size: int | None = Field(default=None, validation_alias="lastSize")
    low_price: float | None = Field(default=None, validation_alias="lowPrice")
    mark: float | None = None
    net_change: float | None = Field(default=None, validation_alias="netChange")
    net_percent_change: float | None = Field(default=None, validation_alias="netPercentChange")
    open_price: float | None = Field(default=None, validation_alias="openPrice")
    quote_time: int | None = Field(default=None, validation_alias="quoteTime")
    security_status: str = Field(default=None, validation_alias="securityStatus")
    tick: int | None = None
    tick_amount: int | None = Field(default=None, validation_alias="tickAmount")
    total_volume: int | None = Field(default=None, validation_alias="totalVolume")
    trade_time: int | None = Field(default=None, validation_alias="tradeTime")


class QuoteResponse(BaseModel):
    asset_main_type: str | None = Field(default=None, validation_alias="assetMainType")
    realtime: bool
    symbol: str
    quote: Quote

    def __str__(self) -> str:
        format_string = f"▪️ {self.symbol}"

        if self.quote.open_price:
            format_string += f", Open: {self.quote.open_price}"

        if self.quote.high_price:
            format_string += f", High: {self.quote.high_price}"

        if self.quote.low_price:
            format_string += f", Low: {self.quote.low_price}"

        if self.quote.close_price:
            format_string += f", Close: {self.quote.close_price}"

        if self.quote.last_price:
            format_string += f", Last: {self.quote.last_price}"

        if self.quote.mark:
            format_string += f", Market: {self.quote.mark}"

        if self.quote.net_percent_change:
            format_string += f", Net Change: {self.quote.net_percent_change:.2f}%"

        format_string += f", 52 Week High: {self.quote.field_52_week_high}"
        format_string += f", 52 Week Low: {self.quote.field_52_week_low}"

        return format_string


class QuoteField(str, Enum):
    QUOTE = "quote"
    FUNDAMENTAL = "fundamental"
    EXTENDED = "extended"
    REFERENCE = "reference"
    REGULAR = "regular"


class QuoteRequest(BaseModel):
    symbols: list[str]
    fields: list[QuoteField] = Field(default=["quote", "reference"])
    indicative: bool = False
