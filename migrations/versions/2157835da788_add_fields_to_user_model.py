"""add fields to user model

Revision ID: 2157835da788
Revises: 54b015f59233
Create Date: 2021-12-28 10:25:44.389860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2157835da788'
down_revision = '54b015f59233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###