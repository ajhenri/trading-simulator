"""

Revision ID: 513e7a73a9fb
Revises: 
Create Date: 2020-02-02 19:32:29.990497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '513e7a73a9fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('trade_type', sa.Enum('buy', 'sell', native_enum=False), nullable=False),
    sa.Column('process_date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=False),
    sa.Column('shares', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.Binary(), nullable=False),
    sa.Column('salt', sa.Binary(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cash_amount', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=True),
    sa.Column('equity_amount', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=True),
    sa.Column('initial_amount', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('bought_at', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=False),
    sa.Column('bought_on', sa.DateTime(), nullable=False),
    sa.Column('sold_on', sa.DateTime(), nullable=True),
    sa.Column('initial_cost', sa.Numeric(precision=19, scale=2, asdecimal=False), nullable=False),
    sa.Column('shares', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=5), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    op.drop_table('accounts')
    op.drop_table('users')
    op.drop_table('trades')
    # ### end Alembic commands ###
