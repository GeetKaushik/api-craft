"""add hashed password to user

Revision ID: a019ab6a5d71
Revises: 48b64bbfdabc
Create Date: 2026-10-19 16:15:16.530260

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "a019ab6a5d71"
down_revision: Union[str, Sequence[str], None] = "48b64bbfdabc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add password hash storage to the existing user table."""
    op.add_column(
        "user",
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    """Remove password hash storage."""
    op.drop_column("user", "hashed_password")
