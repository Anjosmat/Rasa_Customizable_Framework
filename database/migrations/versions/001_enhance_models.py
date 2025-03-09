"""enhance_models

Revision ID: 001
Revises:
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to business_intents
    with op.batch_alter_table('business_intents') as batch_op:
        batch_op.add_column(sa.Column('metadata', sqlite.JSON, nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True),
                                      server_default=sa.text('CURRENT_TIMESTAMP')))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True),
                                      nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(),
                                      server_default='1'))
        batch_op.add_column(sa.Column('priority', sa.Integer(),
                                      server_default='0'))

    # Add new columns to bot_config
    with op.batch_alter_table('bot_config') as batch_op:
        batch_op.add_column(sa.Column('custom_settings', sqlite.JSON,
                                      nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True),
                                      server_default=sa.text('CURRENT_TIMESTAMP')))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True),
                                      nullable=True))
        batch_op.add_column(sa.Column('version', sa.String(),
                                      server_default='1.0.0'))

    # Create custom_responses table
    op.create_table('custom_responses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('intent_id', sa.Integer(), nullable=True),
                    sa.Column('response_type', sa.String(), nullable=True),
                    sa.Column('response_content', sqlite.JSON, nullable=True),
                    sa.Column('conditions', sqlite.JSON, nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('CURRENT_TIMESTAMP')),
                    sa.ForeignKeyConstraint(['intent_id'], ['business_intents.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_custom_responses_id'), 'custom_responses', ['id'],
                    unique=False)

    # Create intent_metadata table
    op.create_table('intent_metadata',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('intent_id', sa.Integer(), nullable=True),
                    sa.Column('key', sa.String(), nullable=True),
                    sa.Column('value', sqlite.JSON, nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('CURRENT_TIMESTAMP')),
                    sa.ForeignKeyConstraint(['intent_id'], ['business_intents.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_intent_metadata_id'), 'intent_metadata', ['id'],
                    unique=False)
    op.create_index(op.f('ix_intent_metadata_key'), 'intent_metadata', ['key'],
                    unique=False)


def downgrade() -> None:
    # Drop new tables
    op.drop_table('intent_metadata')
    op.drop_table('custom_responses')

    # Remove columns from business_intents
    with op.batch_alter_table('business_intents') as batch_op:
        batch_op.drop_column('priority')
        batch_op.drop_column('is_active')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('metadata')

    # Remove columns from bot_config
    with op.batch_alter_table('bot_config') as batch_op:
        batch_op.drop_column('version')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('custom_settings')
