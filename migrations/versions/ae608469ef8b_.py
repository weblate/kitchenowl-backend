"""empty message

Revision ID: ae608469ef8b
Revises: 6d3027e07dc4
Create Date: 2022-06-08 23:27:18.639974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae608469ef8b'
down_revision = '6d3027e07dc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('last_used_at', sa.DateTime(), nullable=True),
    sa.Column('refresh_token_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['refresh_token_id'], ['token.id'], name=op.f('fk_token_refresh_token_id_token')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_token_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_token'))
    )
    with op.batch_alter_table('token', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_jti'), ['jti'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_jti'))

    op.drop_table('token')
    # ### end Alembic commands ###