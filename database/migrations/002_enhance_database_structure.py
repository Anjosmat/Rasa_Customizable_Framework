"""Enhance database structure (add intents and responses tables)

Revision ID: 002_enhance_database_structure
Revises: 001_initial
Create Date: 2025-03-12 16:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_enhance_database_structure'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Create db_intents table
    op.create_table(
        'db_intents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('business_id', sa.Integer, nullable=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('intent_metadata', sa.JSON, nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('priority', sa.Integer, default=0, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )

    # Create db_responses table
    op.create_table(
        'db_responses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('intent_id', sa.Integer, sa.ForeignKey('db_intents.id', ondelete="CASCADE")),
        sa.Column('response_text', sa.Text, nullable=False),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('channel', sa.String(50), nullable=True),
        sa.Column('response_metadata', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )


def downgrade():
    op.drop_table('db_responses')
    op.drop_table('db_intents')
