"""Initial migration

Revision ID: 911a60e32178
Revises: 
Create Date: 2024-03-05 15:48:29.439965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '911a60e32178'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('election', schema=None) as batch_op:
        batch_op.add_column(sa.Column('random_code', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint(None, ['random_code'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('election', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('random_code')

    # ### end Alembic commands ###
