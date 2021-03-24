"""empty message

Revision ID: edf2ed21d285
Revises: bd996cd60504
Create Date: 2021-03-25 03:00:19.371386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edf2ed21d285'
down_revision = 'bd996cd60504'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('league_points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_league_points_group_id'), 'league_points', ['group_id'], unique=False)
    op.create_table('special_points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_special_points_user_id'), 'special_points', ['user_id'], unique=False)
    op.add_column('user_points', sa.Column('memo', sa.String(length=255), nullable=True))
    op.add_column('user_points', sa.Column('reason_class', sa.String(length=255), nullable=True))
    op.add_column('user_points', sa.Column('reason_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_points', 'reason_id')
    op.drop_column('user_points', 'reason_class')
    op.drop_column('user_points', 'memo')
    op.drop_index(op.f('ix_special_points_user_id'), table_name='special_points')
    op.drop_table('special_points')
    op.drop_index(op.f('ix_league_points_group_id'), table_name='league_points')
    op.drop_table('league_points')
    # ### end Alembic commands ###
