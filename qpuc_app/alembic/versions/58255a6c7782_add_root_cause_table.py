"""add root_cause table

Revision ID: 58255a6c7782
Revises: 83141cd329a6
Create Date: 2020-05-09 23:17:31.269940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58255a6c7782'
down_revision = '83141cd329a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guessed_answers', sa.Column('result', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('guessed_answers', 'result')
    # ### end Alembic commands ###