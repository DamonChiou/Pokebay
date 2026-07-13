"""add unique constraint to tcg_product_id

Revision ID: d5cbe8155f95
Revises: d22fbade091a
Create Date: 2026-07-12 18:06:42.572935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5cbe8155f95'
down_revision: Union[str, Sequence[str], None] = 'd22fbade091a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_products_tcg_product_id",
        "products",
        ["tcg_product_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_products_tcg_product_id",
        "products",
        type_="unique"
    )
