"""empty message

Revision ID: 829ba21af148
Revises: 8670660cba55
Create Date: 2020-06-24 23:02:46.418616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829ba21af148'
down_revision = '8670660cba55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board')
    # ### end Alembic commands ###
