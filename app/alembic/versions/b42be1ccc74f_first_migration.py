"""first_migration

Revision ID: b42be1ccc74f
Revises: 
Create Date: 2023-09-12 12:14:51.444481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b42be1ccc74f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emotions_id'), 'emotions', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('configurations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('reminder_frequency', sa.Integer(), nullable=True),
    sa.Column('notifications_enabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configurations_id'), 'configurations', ['id'], unique=False)
    op.create_table('customization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customization_id'), 'customization', ['id'], unique=False)
    op.create_table('emotion_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('emotion_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('intensity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['emotion_id'], ['emotions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emotion_history_id'), 'emotion_history', ['id'], unique=False)
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entries_id'), 'entries', ['id'], unique=False)
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    op.create_table('advanced_analysis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_id', sa.Integer(), nullable=True),
    sa.Column('result', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advanced_analysis_id'), 'advanced_analysis', ['id'], unique=False)
    op.create_table('entry_emotion',
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('emotion_id', sa.Integer(), nullable=False),
    sa.Column('intensity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['emotion_id'], ['emotions.id'], ),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ),
    sa.PrimaryKeyConstraint('entry_id', 'emotion_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry_emotion')
    op.drop_index(op.f('ix_advanced_analysis_id'), table_name='advanced_analysis')
    op.drop_table('advanced_analysis')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_entries_id'), table_name='entries')
    op.drop_table('entries')
    op.drop_index(op.f('ix_emotion_history_id'), table_name='emotion_history')
    op.drop_table('emotion_history')
    op.drop_index(op.f('ix_customization_id'), table_name='customization')
    op.drop_table('customization')
    op.drop_index(op.f('ix_configurations_id'), table_name='configurations')
    op.drop_table('configurations')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_emotions_id'), table_name='emotions')
    op.drop_table('emotions')
    # ### end Alembic commands ###
