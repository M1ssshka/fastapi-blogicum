"""add server_default to created_at

Revision ID: c5579a425f8e
Revises: 98e2a0c45d4f
Create Date: 2026-05-23 12:55:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from application.core.config import settings

# revision identifiers, used by Alembic.
revision: str = 'c5579a425f8e'
down_revision: Union[str, Sequence[str], None] = '98e2a0c45d4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in (
        'blog_post',
        'blog_category',
        'blog_location',
        'blog_comment',
    ):
        op.alter_column(
            table,
            'created_at',
            server_default=sa.text('now()'),
            schema=settings.POSTGRES_SCHEMA,
        )


def downgrade() -> None:
    for table in (
        'blog_post',
        'blog_category',
        'blog_location',
        'blog_comment',
    ):
        op.alter_column(
            table,
            'created_at',
            server_default=None,
            schema=settings.POSTGRES_SCHEMA,
        )
