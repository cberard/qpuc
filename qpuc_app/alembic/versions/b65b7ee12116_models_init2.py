"""Models init2

Revision ID: b65b7ee12116
Revises: deb061041ce2
Create Date: 2020-05-09 23:23:33.224026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b65b7ee12116'
down_revision = 'deb061041ce2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('guessed_answers', 'result')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guessed_answers', sa.Column('result', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
