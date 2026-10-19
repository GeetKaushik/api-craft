"""allow duplicate resource names per owner

Revision ID: 0bce07926faf
Revises: a019ab6a5d71
Create Date: 2026-10-19 17:10:47.098194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bce07926faf'
down_revision: Union[str, Sequence[str], None] = 'a019ab6a5d71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Allow the same resource name for different owners."""

    # Remove the old unique index on resource_name alone.
    op.drop_index(
        "ix_generated_api_resource_name",
        table_name="generated_api",
    )

    # Enforce uniqueness per owner instead.
    op.create_unique_constraint(
        "uq_generated_api_owner_resource",
        "generated_api",
        ["owner_id", "resource_name"],
    )


def downgrade() -> None:
    """Restore globally unique resource names."""

    op.drop_constraint(
        "uq_generated_api_owner_resource",
        "generated_api",
        type_="unique",
    )

    op.create_index(
        "ix_generated_api_resource_name",
        "generated_api",
        ["resource_name"],
        unique=True,
    )
