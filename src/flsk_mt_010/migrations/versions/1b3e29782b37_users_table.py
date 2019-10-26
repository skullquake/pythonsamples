"""users table

Revision ID: 1b3e29782b37
Revises: ad6a4009b0c9
Create Date: 2019-10-24 01:26:38.941509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b3e29782b37'
down_revision = 'ad6a4009b0c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cpu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ts', sa.DateTime(), nullable=True),
    sa.Column('cpu', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cpu')
    # ### end Alembic commands ###
