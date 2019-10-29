"""users table

Revision ID: 7739fe84cf8a
Revises: b8c878b61f4a
Create Date: 2019-10-29 03:28:26.646111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7739fe84cf8a'
down_revision = 'b8c878b61f4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vec2F',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('X', sa.Float(), nullable=True),
    sa.Column('Y', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vec2F')
    # ### end Alembic commands ###
