"""empty message

Revision ID: 3647c9eb1881
Revises: 5140d8f9339b
Create Date: 2023-08-01 23:48:05.570802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3647c9eb1881'
down_revision = '5140d8f9339b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default_key', sa.String(length=128), nullable=True))

    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default_key', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('default_key')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('default_key')

    # ### end Alembic commands ###
