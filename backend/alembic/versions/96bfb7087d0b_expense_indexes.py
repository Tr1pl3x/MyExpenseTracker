"""expense indexes

Revision ID: 96bfb7087d0b
Revises: b9005852c11b
Create Date: 2025-10-03 21:20:29.563353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96bfb7087d0b'
down_revision: Union[str, Sequence[str], None] = 'b9005852c11b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index("idx_expense_user_spent_at", "expense", ["user_id", "spent_at"], unique=False)
    op.create_index("idx_expense_user_cat_spent_at", "expense", ["user_id", "category", "spent_at"], unique=False)

def downgrade():
    op.drop_index("idx_expense_user_cat_spent_at", table_name="expense")
    op.drop_index("idx_expense_user_spent_at", table_name="expense")

