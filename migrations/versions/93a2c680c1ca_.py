"""empty message

Revision ID: 93a2c680c1ca
Revises: 639017653648
Create Date: 2021-08-30 11:48:06.232716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a2c680c1ca'
down_revision = '639017653648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'transaction_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('transaction_type', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    # ### end Alembic commands ###