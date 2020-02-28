"""Extends tables Venue, Artist; adds table Show

Revision ID: f5ad124991c5
Revises: 
Create Date: 2020-02-28 01:40:06.929445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5ad124991c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=300), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=300), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=300), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###
    op.add_tablecreate_table(
      'Show',
      sa.Column('artist_id ', sa.Integer, sa.ForeignKey('Artist.id'), primary_key = True),
      sa.Column('venue_id', sa.Integer, sa.ForeignKey('Venue.id'), primary_key = True),
      sa.Column('start_time ', sa.DateTime)
    )


def downgrade():
    op.drop_table('Show')
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
