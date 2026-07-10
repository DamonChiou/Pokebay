from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pokebay.db.base import Base

if TYPE_CHECKING:
    from pokebay.db.models.product import Product


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    ebay_listing_id: Mapped[str] = mapped_column(String(100), unique=True)
    raw_title: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    url: Mapped[str] = mapped_column(Text)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"), nullable=True
    )

    # ORM relationship — not a column, just a Python convenience.
    # Lets you write listing.product to get the full Product object.
    # back_populates="listings" connects this to Product.listings on the other side.
    product: Mapped["Product | None"] = relationship(back_populates="listings")
