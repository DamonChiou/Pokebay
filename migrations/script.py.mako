"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_products_tcg_product_id",  # constraint name
        "products",                     # table name
        ["tcg_product_id"]             # column(s)
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_products_tcg_product_id",
        "products",
        type_="unique"
    )
