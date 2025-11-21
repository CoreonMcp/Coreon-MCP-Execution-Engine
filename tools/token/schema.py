from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ChangeData(BaseModel):
    change: int
    changePercent: float

class SupplyTier(BaseModel):
    supply: str
    supplyPercent: float

class HolderChange(BaseModel):
    min5: ChangeData
    h1: ChangeData
    h6: ChangeData
    d1: ChangeData
    d3: ChangeData
    d7: ChangeData
    d30: ChangeData

class HolderSupply(BaseModel):
    top10: SupplyTier
    top25: SupplyTier
    top50: SupplyTier
    top100: SupplyTier
    top250: SupplyTier
    top500: SupplyTier

class HolderDistribution(BaseModel):
    whales: int
    sharks: int
    dolphins: int
    fish: int
    octopus: int
    crabs: int
    shrimps: int

class TokenVolumeStats(BaseModel):
    min5: float
    h1: float
    h4: float
    d1: float

class TokenCountStats(BaseModel):
    min5: int
    h1: int
    h4: int
    d1: int

class GetTokenParams(BaseModel):
    contract_address: str = Field(..., description="Token contract address")
    chain: str = Field(..., description="Blockchain name (e.g., bsc)")

class GetWalletTokensParams(BaseModel):
    address: str = Field(..., description="Token Address")

class GetMyWalletAddressParams(BaseModel):
    wallet_address: str = Field(..., description="my wallet address")

class GetPriceResponse(BaseModel):
    tokenName: str
    tokenSymbol: str
    usdPriceFormatted: str
    exchangeName: str
    usdPrice24hrUsdChange: float
    usdPrice24hrPercentChange: float

class GetTokensResponse(BaseModel):
    token_address: str
    symbol: str
    balance: str
    usd_price: float
    usd_value: float
    price_change_24hr_percent: float
    price_change_24hr_usd: float
    security_score: int
    is_verified: bool
    is_native: bool

class GetNativeBalanceResponse(BaseModel):
    balance: str

class GetTokenMetadataResponse(BaseModel):
    symbol: str
    total_supply_formatted: str
    fully_diluted_valuation: str
    validated: int
    created_at: str
    security_score: int
    circulating_supply: str
    market_cap: str

class GetTokenOwnershipResponse(BaseModel):
    balance_formatted: str
    owner_address: str
    percentage_relative_to_total_supply: float

class GetHolderSummaryResponse(BaseModel):
    totalHolders: int
    holdersByAcquisition: Dict[str, int]
    holderChange: HolderChange
    holderSupply: HolderSupply
    holderDistribution: HolderDistribution

class GetTokenPairStatsResponse(BaseModel):
    token_address: str
    total_liquidity_usd: float
    total_active_pairs: int
    total_active_dexes: int

    total_swaps: TokenCountStats
    total_volume: TokenVolumeStats
    total_buy_volume: TokenVolumeStats
    total_sell_volume: TokenVolumeStats
    total_buyers: TokenCountStats
    total_sellers: TokenCountStats

class GetTokenSocialsResponse(BaseModel):
    symbol: str
    name: str
    twitter: str = Field(..., description="Twitter profile link")
    user_handle: str = Field(..., description="Twitter handle")

class GetMyWalletAddressResponse(BaseModel):
    wallet_address: str