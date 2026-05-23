"""add refresh token

Revision ID: 98e2a0c45d4f
Revises: 1d27fd882600
Create Date: 2026-05-23 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from application.core.config import settings

# revision identifiers, used by Alembic.
revision: str = '98e2a0c45d4f'
down_revision: Union[str, Sequence[str], None] = '1d27fd882600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'auth_refresh_token',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            'token_hash',
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column('is_revoked', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            [f'{settings.POSTGRES_SCHEMA}.auth_user.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA,
    )
    op.create_index(
        'ix_auth_refresh_token_token_hash',
        'auth_refresh_token',
        ['token_hash'],
        unique=True,
        schema=settings.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index(
        'ix_auth_refresh_token_token_hash',
        table_name='auth_refresh_token',
        schema=settings.POSTGRES_SCHEMA,
    )
    op.drop_table('auth_refresh_token', schema=settings.POSTGRES_SCHEMA)
