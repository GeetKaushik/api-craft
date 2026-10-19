
"""add archived status to generated api

Revision ID: 9e22113ae576
Revises: 0bce07926faf
"""

from alembic import op
import sqlalchemy as sa


revision = "9e22113ae576"
down_revision = "0bce07926faf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "generated_api",
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    # Remove the temporary database default after existing rows
    # have received False, while keeping the model default.
    op.alter_column(
        "generated_api",
        "is_archived",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("generated_api", "is_archived")
