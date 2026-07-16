import asyncio
from rapidfuzz import fuzz, process
from sqlalchemy import select
from pokebay.db.engine import AsyncSessionLocal
from pokebay.db.models.listing import Listing
from pokebay.db.models.product import Product

MATCH_THRESHOLD = 85


async def match_listings() -> None:
    async with AsyncSessionLocal() as session:
        products = (await session.execute(select(Product))).scalars().all()
        product_names = {product.id: product.name for product in products}

        unmatched = (
            await session.execute(select(Listing).where(Listing.product_id.is_(None)))
        ).scalars().all()

        for listing in unmatched:
            match = process.extractOne(
                listing.raw_title,
                product_names,
                scorer=fuzz.token_set_ratio,
            )
            if match is None:
                continue

            _, score, product_id = match
            if score >= MATCH_THRESHOLD:
                listing.product_id = product_id

        await session.commit()

    print("Matching complete.")


def main() -> None:
    asyncio.run(match_listings())


if __name__ == "__main__":
    main()
