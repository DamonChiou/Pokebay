import httpx

# Pokemon TCG API — free, no auth required, 1000 requests/day limit
SEARCH_URL = "https://api.pokemontcg.io/v2/cards"


async def search_card_price(card_name: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            SEARCH_URL,
            params={"q": f'name:"{card_name}"'},
        )

        response.raise_for_status()
        data = response.json()

        return [parse_card(card) for card in data.get("data", [])]


def parse_card(raw: dict) -> dict:
    # prices lives nested under tcgplayer.prices
    # each card can have multiple price types (holofoil, normal, reverseHolofoil)
    # we grab the whole prices dict and let the caller decide which type they need
    tcgplayer = raw.get("tcgplayer", {})
    prices = tcgplayer.get("prices", {})

    return {
        "name": raw.get("name", ""),
        "set_name": raw.get("set", {}).get("name", ""),
        "tcg_product_id": str(raw.get("id", "")),
        "prices": prices,
    }
