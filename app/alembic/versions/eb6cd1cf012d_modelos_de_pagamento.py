"""Modelos de pagamento

Revision ID: eb6cd1cf012d
Revises: 5eb9691a9ef4
Create Date: 2025-10-29 14:05:33.097486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb6cd1cf012d'
down_revision: Union[str, Sequence[str], None] = '5eb9691a9ef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
