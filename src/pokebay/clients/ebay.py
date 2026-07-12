import base64
import httpx
from pokebay.config import settings
from decimal import Decimal


# eBay's OAuth token endpoint — we POST here to get a temporary access token
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# eBay's Browse API — this is what we use to search listings
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# The scope tells eBay what permissions we need — public read-only access
SCOPE = "https://api.ebay.com/oauth/api_scope"


async def _get_access_token(client: httpx.AsyncClient) -> str:
    # OAuth requires App ID and Client Secret to be base64 encoded together
    # Format is "AppID:ClientSecret" encoded to base64
    credentials = f"{settings.ebay_app_id}:{settings.ebay_client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()

    response = await client.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": SCOPE,
        },
    )

    # Raises an exception if eBay returned an error status (4xx, 5xx)
    response.raise_for_status()

    return response.json()["access_token"]


async def search_listings(query: str, limit: int = 50) -> list[dict]:
    # httpx.AsyncClient is like a browser session — reuses the connection
    # for multiple requests instead of opening a new one each time
    async with httpx.AsyncClient() as client:
        token = await _get_access_token(client)

        response = await client.get(
            SEARCH_URL,
            headers={"Authorization": f"Bearer {token}"},
            params={
                "q": query,
                "limit": limit,
                # filter to Buy It Now listings only — auctions have unpredictable prices
                "filter": "buyingOptions:{FIXED_PRICE}",
            },
        )

        response.raise_for_status()
        data = response.json()

        # eBay returns results under "itemSummaries" key
        # if no results found, default to empty list
        raw_listings = data.get("itemSummaries", [])
        return [parse_listing(item) for item in raw_listings]
    

def parse_listing(raw: dict) -> dict:
    # eBay returns price as a nested dict with a string value
    # {"value": "45.00", "currency": "USD"}
    # We convert the string to Decimal for exact money math
    price_str = raw.get("price", {}).get("value", "0")

    return {
        "ebay_listing_id": raw.get("itemId", ""),
        "raw_title": raw.get("title", ""),
        "price": Decimal(price_str),
        "url": raw.get("itemWebUrl", ""),
    }
