import asyncio
from sqlalchemy.dialects.postgresql import insert
from pokebay.db.engine import AsyncSessionLocal
from pokebay.db.models.listing import Listing
from pokebay.db.models.product import Product
from pokebay.clients.ebay import search_listings
from pokebay.clients.tcgplayer import search_card_price

# The cards we search for on eBay and TCGPlayer.
# Expand this list as you want to track more cards.
SEARCH_TERMS = [
    "Charizard VMAX",
    "Pikachu VMAX",
    "Umbreon VMAX",
]


async def ingest_listings(term: str) -> None:
    # Fetch raw listings from eBay for this search term
    listings = await search_listings(term, limit=50)

    async with AsyncSessionLocal() as session:
        for listing in listings:
            # insert().on_conflict_do_nothing() is the upsert —
            # if a listing with this ebay_listing_id already exists, skip it.
            # Prevents duplicates when the runner executes multiple times.
            stmt = (
                insert(Listing)
                .values(
                    ebay_listing_id=listing["ebay_listing_id"],
                    raw_title=listing["raw_title"],
                    price=listing["price"],
                    url=listing["url"],
                )
                .on_conflict_do_nothing(index_elements=["ebay_listing_id"])
            )
            await session.execute(stmt)

        # Commit all listings for this search term in one transaction
        await session.commit()

    print(f"Ingested listings for: {term}")


async def ingest_products(term: str) -> None:
    # Fetch card data + market prices from Pokemon TCG API
    cards = await search_card_price(term)

    async with AsyncSessionLocal() as session:
        for card in cards:
            # For products, upsert on tcg_product_id —
            # if we've seen this card before, update its market price.
            # Prices change daily so we always want the latest value.
            holofoil_price = card["prices"].get("holofoil", {}).get("market")

            stmt = (
                insert(Product)
                .values(
                    name=card["name"],
                    product_type="card",
                    set_name=card["set_name"],
                    tcg_product_id=card["tcg_product_id"],
                    tcg_market_price=holofoil_price,
                )
                .on_conflict_do_update(
                    index_elements=["tcg_product_id"],
                    # on conflict, only update the price — don't overwrite name/set
                    set_={"tcg_market_price": holofoil_price},
                )
            )
            await session.execute(stmt)

        await session.commit()

    print(f"Ingested products for: {term}")


async def run_pipeline() -> None:
    # Run ingestion for every search term sequentially
    for term in SEARCH_TERMS:
        await ingest_listings(term)
        await ingest_products(term)
        print(f"Pipeline complete for: {term}")


def main() -> None:
    asyncio.run(run_pipeline())


if __name__ == "__main__":
    main()
