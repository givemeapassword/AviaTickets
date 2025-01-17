"""Add users, countries, and season_factors

Revision ID: 827911cfde18
Revises: 
Create Date: 2024-11-14 17:37:02.238168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827911cfde18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создание таблиц
    op.create_table('countries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country_name', sa.String(length=50), nullable=False),
        sa.Column('flight', sa.Float(), nullable=False),
        sa.Column('accommodation', sa.Float(), nullable=False),
        sa.Column('food', sa.Float(), nullable=False),
        sa.Column('transport', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('country_name')
    )
    
    op.create_table('season_factors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('season', sa.String(length=20), nullable=False),
        sa.Column('factor', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('season')
    )
    
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    

    op.execute("""
        INSERT INTO countries (country_name, flight, accommodation, food, transport)
        VALUES
        ('USA', 500, 100, 50, 30),
        ('France', 400, 120, 60, 40),
        ('Japan', 600, 150, 70, 50),
        ('Germany', 550, 110, 55, 35),
        ('Italy', 450, 130, 65, 45),
        ('Australia', 700, 160, 80, 60);
    """)


    op.execute("""
        INSERT INTO season_factors (season, factor)
        VALUES
        ('summer', 1.2),
        ('winter', 1.5),
        ('offseason', 0.8),
        ('spring', 1.1),
        ('autumn', 1.0);
    """)

def downgrade():
    # Удаление таблиц
    op.drop_table('users')
    op.drop_table('season_factors')
    op.drop_table('countries')
