"""calorie model fixed relations

Revision ID: cc87b02bc995
Revises: 3d7da76f7950
Create Date: 2022-01-19 12:33:42.596414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc87b02bc995'
down_revision = '3d7da76f7950'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('calories_dish_id_fkey', 'calories', type_='foreignkey')
    op.drop_constraint('calories_user_id_fkey', 'calories', type_='foreignkey')
    op.drop_column('calories', 'user_id')
    op.drop_column('calories', 'dish_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calories', sa.Column('dish_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('calories', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('calories_user_id_fkey', 'calories', 'users', ['user_id'], ['id'])
    op.create_foreign_key('calories_dish_id_fkey', 'calories', 'dishes', ['dish_id'], ['id'])
    # ### end Alembic commands ###
