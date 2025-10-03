"""constraints: amount_nonneg, currency_len3

Revision ID: 39c6c3161f07
Revises: 73c9956d6d10
Create Date: 2025-10-03 23:28:09.925142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39c6c3161f07'
down_revision: Union[str, Sequence[str], None] = '73c9956d6d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # currency CHAR(3) and non-negative amount
    # 1) change type of currency to VARCHAR(3) (portable) then add check
    op.alter_column("expense", "currency", type_=sa.String(length=3), existing_type=sa.String())
    op.create_check_constraint("ck_expense_amount_nonneg", "expense", "amount_cents >= 0")
    op.create_check_constraint("ck_expense_currency_len3", "expense", "char_length(currency) = 3")


def downgrade():
    op.drop_constraint("ck_expense_currency_len3", "expense", type_="check")
    op.drop_constraint("ck_expense_amount_nonneg", "expense", type_="check")
    # optional: widen currency back (if you want)
    op.alter_column("expense", "currency", type_=sa.String())