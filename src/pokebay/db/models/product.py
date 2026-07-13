from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pokebay.db.base import Base

if TYPE_CHECKING:
    from pokebay.db.models.listing import Listing


# This "Product" class is "reference data", which is stable and referenced by the "event data", 
# which is the "Listings" table
# This is an "ORM model" or a "Mapped Class" is a blueprint 
# that shows the structure of a schema

# CONVENTIONAL STRUCTURE: column name: Mapped[type in python] = mapped_column(type in sql)

class Product(Base):
    __tablename__ = "products"

    # primary_key=True, Postgres with auto-increment this, never set manually

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    product_type: Mapped[str] = mapped_column(String(50))
    set_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tcg_market_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tcg_product_id: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    listings: Mapped[list["Listing"]] = relationship(back_populates="product")

