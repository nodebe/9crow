"""empty message

Revision ID: bec789179f73
Revises: 757ce554612b
Create Date: 2021-08-29 06:23:11.530606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bec789179f73'
down_revision = '757ce554612b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fullname', sa.String(length=30), nullable=True))
    op.drop_column('user', 'fullnam')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fullnam', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    op.drop_column('user', 'fullname')
    # ### end Alembic commands ###
