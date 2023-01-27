"""initial

Revision ID: b4167d9dc1d2
Revises: e47fe77fab66
Create Date: 2023-01-24 16:38:19.866535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4167d9dc1d2'
down_revision = 'e47fe77fab66'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('submenus_count', sa.Integer(), nullable=True),
    sa.Column('dishes_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('submenu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('dishes_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('dish',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Float(precision=2), nullable=True),
    sa.Column('submenu_id', sa.Integer(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
