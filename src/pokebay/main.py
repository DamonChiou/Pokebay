from pathlib import Path
from decimal import Decimal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pokebay.scoring.deal_scorer import find_deals

app = FastAPI()


class DealOut(BaseModel):
    product_name: str
    listing_price: Decimal
    market_price: Decimal
    discount_pct: Decimal
    listing_url: str


@app.get("/deals", response_model=list[DealOut])
async def get_deals() -> list[DealOut]:
    deals = await find_deals()
    results = []
    for deal in deals:
        assert deal.product.tcg_market_price is not None
        results.append(
            DealOut(
                product_name=deal.product.name,
                listing_price=deal.listing.price,
                market_price=deal.product.tcg_market_price,
                discount_pct=deal.discount_pct,
                listing_url=deal.listing.url,
            )
        )
    return results


STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")