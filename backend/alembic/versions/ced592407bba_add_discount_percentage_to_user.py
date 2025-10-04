"""Add discount_percentage to User

Revision ID: ced592407bba
Revises: c9d818cb1a4c
Create Date: 2025-10-04 13:59:58.906496
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ced592407bba'
down_revision = 'c9d818cb1a4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema: add discount_percentage to users."""
    op.add_column(
        'users',
        sa.Column(
            'discount_percentage',
            sa.Integer(),
            nullable=False,
            server_default='0'  # default to 0 for existing users
        )
    )


def downgrade() -> None:
    """Downgrade schema: remove discount_percentage from users."""
    op.drop_column('users', 'discount_percentage')
