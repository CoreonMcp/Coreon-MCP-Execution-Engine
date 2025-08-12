from .schema import GetUserHandleInfoParams, GetUserIDInfoParams, GetUserTweetsParams
import httpx
from config.settings import settings

BASE_URL = settings.PROXY_BASE_URL

async def get_user_handle_info(params: GetUserHandleInfoParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/twitter/userhandleinfo",
                json={"user_handle": params.user_handle}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_user_id_info(params: GetUserIDInfoParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/twitter/useridinfo",
                json={"user_id": params.user_id}
            )
            data = resp.json()
            return data
    except Exception as e:
        return {"error": str(e)}

async def get_user_tweets(params: GetUserTweetsParams):
    try:
        payload = {}
        if params.link:
            payload["link"] = params.link
            payload["user_id"] = ''
        if params.user_id:
            payload["user_id"] = params.user_id
            payload["link"] = ''
        if params.user_id and params.link:
            payload["user_id"] = params.user_id
            payload["link"] = params.link

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/twitter/twittertweets",
                json=payload
            )
            data = resp.json()
            return data

    except Exception as e:
        return {"error": str(e)}

async def get_twitter_check_follow(params: GetUserTweetsParams):
    try:
        payload = {}
        if params.project_handle:
            payload["project_handle"] = params.project_handle
            payload["project_id"] = ''
        if params.project_id:
            payload["project_handle"] = ''
            payload["project_id"] = params.project_id
        if params.user_handle:
            payload["user_handle"] = params.user_handle
            payload["user_id"] = ''
        if params.user_id:
            payload["user_handle"] = ''
            payload["user_id"] = params.user_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/proxy/twitter/checkfollow",
                json=payload
            )
            data = resp.json()
            return data

    except Exception as e:
        return {"error": str(e)}
