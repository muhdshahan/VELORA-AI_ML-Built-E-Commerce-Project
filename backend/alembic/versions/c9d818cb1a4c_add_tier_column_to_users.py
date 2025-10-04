from alembic import op
import sqlalchemy as sa

revision = 'c9d818cb1a4c'
down_revision = '3929e0f2f238'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add 'tier' column
    op.add_column('users', sa.Column('tier', sa.String(length=50), nullable=True))

def downgrade() -> None:
    # Remove 'tier' column
    op.drop_column('users', 'tier')
