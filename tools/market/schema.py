from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class RecentData(BaseModel):
    Open_Time: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float
    EMA_5: float
    EMA_10: float
    EMA_20: float
    EMA_50:float
    RSI_14: float
    MACD_12_26_9: float
    MACDh_12_26_9: float
    MACDs_12_26_9: float
    STOCHk_14_3_3: float
    STOCHd_14_3_3: float
    CCI_14_0: float
    OBV: float
    ATRr_14: float
    BBL_20_2:float
    BBM_20_2:float
    BBU_20_2:float
    BBB_20_2:float
    BBP_20_2:float

class Summary(BaseModel):
    highest_price: float
    lowest_price: float
    average_close: float
    amplitude: float
    current_close: float
    current_rsi: float
    current_macd: float
    current_obv: float

class GetSymbolKlineDataParams(BaseModel):
    symbol: str = Field(..., description="Token symbol no address")

class GetSymbolKlineDataResponse(BaseModel):
    short_interval: str
    short_recent_data: RecentData
    long_interval: str
    long_recent_data: RecentData
    short_summary: Summary
    long_summary: Summary

class GetSymbolFetchNewsParams(BaseModel):
    symbol: str = Field(..., description="Token symbol no address")

class GetSymbolFetchNewsResponse(BaseModel):
    title: str
    published_at: str

class GetSymbolPriceParams(BaseModel):
    symbol: str = Field(..., description="Token symbol no address")

class GetSymbolPriceResponse(BaseModel):
    symbol: str
    price: str
