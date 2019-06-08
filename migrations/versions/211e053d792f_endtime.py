"""endtime

Revision ID: 211e053d792f
Revises: 37b1d6074517
Create Date: 2019-06-08 18:33:59.705513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '211e053d792f'
down_revision = '37b1d6074517'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('endtime', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_group_endtime'), 'group', ['endtime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_group_endtime'), table_name='group')
    op.drop_column('group', 'endtime')
    # ### end Alembic commands ###
