"""empty message

Revision ID: 2522eb38baae
Revises: cb01788112ec
Create Date: 2019-05-28 17:28:58.269236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2522eb38baae'
down_revision = 'cb01788112ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enter_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(length=14), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enter_group_uid'), 'enter_group', ['uid'], unique=True)
    op.drop_index('ix_idworker_uid', table_name='idworker')
    op.drop_table('idworker')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('idworker',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uid', sa.VARCHAR(length=14), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_idworker_uid', 'idworker', ['uid'], unique=1)
    op.drop_index(op.f('ix_enter_group_uid'), table_name='enter_group')
    op.drop_table('enter_group')
    # ### end Alembic commands ###
