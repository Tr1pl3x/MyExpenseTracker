"""expense.category_id fk and backfill

Revision ID: 73c9956d6d10
Revises: 2f44607e084e
Create Date: 2025-10-03 22:33:42.500407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73c9956d6d10'
down_revision: Union[str, Sequence[str], None] = '2f44607e084e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # add column + FK
    op.add_column("expense", sa.Column("category_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_expense_category", "expense", "category", ["category_id"], ["id"])

    # (optional) drop old index if you created it earlier for text category
    op.execute('DROP INDEX IF EXISTS idx_expense_user_cat_spent_at')

    # new index for queries by category_id
    op.create_index(
        "idx_expense_user_catid_spent_at",
        "expense", ["user_id", "category_id", "spent_at"],
        unique=False
    )

    # backfill category_id from old text column
    op.execute("""
        UPDATE expense e
        SET category_id = c.id
        FROM category c
        WHERE c.user_id = e.user_id
          AND lower(coalesce(e.category, '')) = c.normalized_name
    """)

def downgrade():
    op.drop_index("idx_expense_user_catid_spent_at", table_name="expense")
    op.drop_constraint("fk_expense_category", "expense", type_="foreignkey")
    op.drop_column("expense", "category_id")