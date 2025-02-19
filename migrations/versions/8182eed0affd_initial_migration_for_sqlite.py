"""Initial migration for SQLite

Revision ID: 8182eed0affd
Revises: 
Create Date: 2025-02-19 15:57:28.128083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8182eed0affd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('price_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('update_count', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('table_update_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('update_count', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price_table_id', sa.Integer(), nullable=False),
    sa.Column('old_data', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['price_table_id'], ['price_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item')
    op.drop_table('price_history')
    op.drop_table('order')
    op.drop_table('user')
    op.drop_table('table_update_log')
    op.drop_table('price_table')
    op.drop_table('news')
    # ### end Alembic commands ###
