"""empty message

Revision ID: 46749fb07988
Revises: e51bba3963cf
Create Date: 2020-06-07 23:18:36.346910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46749fb07988'
down_revision = 'e51bba3963cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_role_user', sa.Column('cms_user_id', sa.Integer(), nullable=False))
    op.drop_constraint('cms_role_user_ibfk_1', 'cms_role_user', type_='foreignkey')
    op.create_foreign_key(None, 'cms_role_user', 'cms_role', ['cms_role_id'], ['id'])
    op.create_foreign_key(None, 'cms_role_user', 'cms_user', ['cms_user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cms_role_user', type_='foreignkey')
    op.drop_constraint(None, 'cms_role_user', type_='foreignkey')
    op.create_foreign_key('cms_role_user_ibfk_1', 'cms_role_user', 'cms_user', ['cms_role_id'], ['id'])
    op.drop_column('cms_role_user', 'cms_user_id')
    # ### end Alembic commands ###