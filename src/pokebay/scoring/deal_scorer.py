import asyncio
from dataclasses import dataclass
from decimal import Decimal
from sqlalchemy import select
from pokebay.db.engine import AsyncSessionLocal
from pokebay.db.models.listing import Listing
from pokebay.db.models.product import Product

# A listing must be at least this fraction below TCGPlayer market price
# to count as a deal. 0.30 = 30% off.
DISCOUNT_THRESHOLD = Decimal("0.30")


@dataclass
class Deal:
    listing: Listing
    product: Product
    discount_pct: Decimal


async def find_deals() -> list[Deal]:
    async with AsyncSessionLocal() as session:
        rows = (
            await session.execute(
                select(Listing, Product)
                .join(Product, Listing.product_id == Product.id)
                .where(Product.tcg_market_price.is_not(None))
            )
        ).all()

        deals = []
        for listing, product in rows:
            market_price = product.tcg_market_price
            discount_pct = (market_price - listing.price) / market_price

            if discount_pct >= DISCOUNT_THRESHOLD:
                deals.append(Deal(listing=listing, product=product, discount_pct=discount_pct))

        return deals


def main() -> None:
    deals = asyncio.run(find_deals())
    for deal in deals:
        print(
            f"{deal.product.name}: ${deal.listing.price} vs market ${deal.product.tcg_market_price} "
            f"({deal.discount_pct:.0%} off) -> {deal.listing.url}"
        )
    print(f"{len(deals)} deal(s) found.")


if __name__ == "__main__":
    main()
