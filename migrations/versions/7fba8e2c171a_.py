"""empty message

Revision ID: 7fba8e2c171a
Revises: 1af1fb1c355f
Create Date: 2021-08-29 16:13:39.963492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fba8e2c171a'
down_revision = '1af1fb1c355f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('account_status', sa.String(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'account_status')
    # ### end Alembic commands ###