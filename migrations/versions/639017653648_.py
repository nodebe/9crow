"""empty message

Revision ID: 639017653648
Revises: 7fba8e2c171a
Create Date: 2021-08-30 11:18:24.627583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '639017653648'
down_revision = '7fba8e2c171a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('transaction_type', sa.String(length=10), nullable=True))
    op.add_column('transaction', sa.Column('transaction_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'transaction_date')
    op.drop_column('transaction', 'transaction_type')
    # ### end Alembic commands ###