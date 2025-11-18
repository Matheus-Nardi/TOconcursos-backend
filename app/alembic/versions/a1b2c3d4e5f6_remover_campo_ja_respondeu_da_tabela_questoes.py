"""remover campo ja_respondeu da tabela questoes

Revision ID: a1b2c3d4e5f6
Revises: 2f3a9becb9fa
Create Date: 2025-01-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '2f3a9becb9fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove a coluna ja_respondeu da tabela questoes."""
    op.drop_column('questoes', 'ja_respondeu')


def downgrade() -> None:
    """Reverte a remoção da coluna ja_respondeu."""
    op.add_column('questoes', sa.Column('ja_respondeu', sa.Boolean(), nullable=True))

