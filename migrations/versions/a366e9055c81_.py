"""empty message

Revision ID: a366e9055c81
Revises: 
Create Date: 2020-09-12 15:54:45.620905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a366e9055c81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('hit', sa.Integer(), nullable=True),
    sa.Column('access', sa.Boolean(), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
