"""create orders table

Revision ID: 3929e0f2f238
Revises: 1758b79f3c40
Create Date: 2025-10-04 10:08:51.730493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3929e0f2f238'
down_revision: Union[str, Sequence[str], None] = '1758b79f3c40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
