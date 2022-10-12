"""empty message

Revision ID: f5e57e0202fe
Revises: 71d2611d92f7
Create Date: 2022-10-08 18:49:49.184585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e57e0202fe'
down_revision = '71d2611d92f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'comments', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    # ### end Alembic commands ###