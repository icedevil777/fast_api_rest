"""initial

Revision ID: 99260a7ad50e
Revises: c82fcf26ede6
Create Date: 2023-01-25 18:59:04.061127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99260a7ad50e'
down_revision = 'c82fcf26ede6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dish_title_key', 'dish', type_='unique')
    op.drop_constraint('menu_title_key', 'menu', type_='unique')
    op.drop_constraint('submenu_title_key', 'submenu', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('submenu_title_key', 'submenu', ['title'])
    op.create_unique_constraint('menu_title_key', 'menu', ['title'])
    op.create_unique_constraint('dish_title_key', 'dish', ['title'])
    # ### end Alembic commands ###
