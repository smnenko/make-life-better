"""nickname to username

Revision ID: dc6cd389e341
Revises: 07524eb5e149
Create Date: 2021-11-29 16:13:53.402534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc6cd389e341'
down_revision = '07524eb5e149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=16), nullable=True))
    op.drop_constraint('users_nickname_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.VARCHAR(length=16), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_nickname_key', 'users', ['nickname'])
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
