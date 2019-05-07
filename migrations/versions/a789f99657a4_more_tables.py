"""more tables

Revision ID: a789f99657a4
Revises: 146b24582d8a
Create Date: 2019-05-07 20:09:35.126767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a789f99657a4'
down_revision = '146b24582d8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bookname', sa.String(length=64), nullable=True),
    sa.Column('remain', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_bookname'), 'book', ['bookname'], unique=True)
    op.create_index(op.f('ix_book_remain'), 'book', ['remain'], unique=False)
    op.create_table('borrow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('borrow_num', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('isadmin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isadmin')
    op.drop_table('card')
    op.drop_table('borrow')
    op.drop_index(op.f('ix_book_remain'), table_name='book')
    op.drop_index(op.f('ix_book_bookname'), table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###
