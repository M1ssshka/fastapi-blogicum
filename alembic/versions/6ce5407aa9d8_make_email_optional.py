"""make_email_optional

Revision ID: 6ce5407aa9d8
Revises: 869df2353e62
Create Date: 2026-04-20 12:29:05.645106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce5407aa9d8'
down_revision: Union[str, Sequence[str], None] = '869df2353e62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # For SQLite, we need to recreate the table with nullable email
    # batch_alter_table handles this automatically
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.alter_column('email',
                              existing_type=sa.String(),
                              nullable=True)
    
    # After making column nullable, update empty strings to NULL
    op.execute("UPDATE auth_user SET email = NULL WHERE email = ''")


def downgrade() -> None:
    """Downgrade schema."""
    # Make email column non-nullable again
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.alter_column('email',
                              existing_type=sa.String(),
                              nullable=False)
