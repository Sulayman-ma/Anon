"""Removed brand car field

Revision ID: c1b6465d1661
Revises: 1dcfa98579bb
Create Date: 2022-06-08 22:48:30.620354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1b6465d1661'
down_revision = '1dcfa98579bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('brand')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('brand', sa.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###
