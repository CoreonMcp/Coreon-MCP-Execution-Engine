from .schema import GetTokenParams, GetWalletTokensParams, GetMyWalletAddressParams
import httpx
from config.settings import settings

BASE_URL = settings.PROXY_BASE_URL

async def get_price(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/token/price",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data.get("data") or data
    except Exception as e:
        return {"error": str(e)}

async def get_tokens(params: GetWalletTokensParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/wallet/tokens",
                json={"address": params.address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_native_balance(params: GetWalletTokensParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/wallet/nativebalance",
                json={"address": params.address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_token_metadata(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/token/metadata",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_token_ownership(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/token/owner",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_holder_summary(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/token/holder",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_token_pair_stats(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/bsc/token/pairsstats",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_token_socials(params: GetTokenParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/token/socials",
                json={"token_address": params.contract_address}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_my_wallet_address(params: GetMyWalletAddressParams):
    return {"success": True, "data": {"wallet_address": params.wallet_address}}



