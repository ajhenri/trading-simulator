"""update username to email

Revision ID: 2e59716e1ee4
Revises: f36a535bc8d0
Create Date: 2020-02-16 21:27:03.227571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e59716e1ee4'
down_revision = 'f36a535bc8d0'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('users', 'username', nullable=False, type_=sa.String(length=254), new_column_name='email')

def downgrade():
    op.alter_column('users', 'email', nullable=False, type_=sa.String(length=80), new_column_name='username')
