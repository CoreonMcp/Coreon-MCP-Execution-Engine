from .schema import GetSymbolKlineDataParams, GetSymbolFetchNewsParams, GetSymbolPriceParams
import httpx
from config.settings import settings

BASE_URL = settings.PROXY_BASE_URL

async def get_symbol_kline_data(params: GetSymbolKlineDataParams):
    try:
        symbol = f"{params.symbol}USDT"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/makret/getklinefeatureextractor",
                json={"symbol": symbol}
            )
            data = resp.json()
            return data
    except Exception as e:
        import traceback
        error_message = f"{type(e).__name__}: {str(e)}"
        print("Exception Trace:", traceback.format_exc())
        return {"error": error_message}

async def get_symbol_fetch_news(params: GetSymbolFetchNewsParams):
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/cryptopanic/fetchnews",
                json={"keyword": params.symbol}
            )
            data = resp.json()
            return data
    except Exception as e:
        import traceback
        error_message = f"{type(e).__name__}: {str(e)}"
        print("Exception Trace:", traceback.format_exc())
        return {"error": error_message}

async def get_symbol_price(params: GetSymbolPriceParams):
    try:
        symbol = f"{params.symbol}USDT"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/makret/getsymbolprice",
                json={"symbol": symbol}
            )
            data = resp.json()
            return data
    except Exception as e:
        import traceback
        error_message = f"{type(e).__name__}: {str(e)}"
        print("Exception Trace:", traceback.format_exc())
        return {"error": error_message}