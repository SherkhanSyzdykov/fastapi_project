"""url and request tables created

Revision ID: 6aa0125448e5
Revises: 
Create Date: 2022-03-12 17:32:59.713611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa0125448e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('request',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('url_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['url_id'], ['url.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('url')
    # ### end Alembic commands ###