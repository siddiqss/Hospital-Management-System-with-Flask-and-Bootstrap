"""timestamp addeed in patient model

Revision ID: c5ea67d2f81f
Revises: 168ea345ad20
Create Date: 2020-12-29 18:40:11.578562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5ea67d2f81f'
down_revision = '168ea345ad20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patient', 'timestamp')
    # ### end Alembic commands ###
