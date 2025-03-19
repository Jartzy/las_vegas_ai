"""New schema

Revision ID: new_schema_2025
Revises: 
Create Date: 2025-03-19 18:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'new_schema_2025'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table first
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(80), nullable=False),
        sa.Column('password_hash', sa.String(128), nullable=False),
        sa.Column('otp_secret', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    # Create affiliates table
    op.create_table('affiliates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('api_key', sa.String(255), nullable=True),
        sa.Column('commission_rate', sa.Float(), nullable=True),
        sa.Column('categories', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create events table
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(255), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('subcategory', sa.String(100), nullable=True),
        sa.Column('price_range_min', sa.Numeric(10, 2), nullable=True),
        sa.Column('price_range_max', sa.Numeric(10, 2), nullable=True),
        sa.Column('venue', sa.String(255), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('source', sa.String(50), nullable=True),
        sa.Column('rating', sa.Numeric(3, 2), nullable=True),
        sa.Column('review_count', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('casino', sa.String(255), nullable=True),
        sa.Column('age_restriction', sa.Integer(), nullable=True),
        sa.Column('dress_code', sa.String(100), nullable=True),
        sa.Column('parking_info', sa.Text(), nullable=True),
        sa.Column('reservation_required', sa.Boolean(), nullable=True),
        sa.Column('indoor_outdoor', sa.String(20), nullable=True),
        sa.Column('typical_duration', sa.Integer(), nullable=True),
        sa.Column('best_times', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('amenities', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('difficulty_level', sa.String(20), nullable=True),
        sa.Column('seasonal_info', sa.Text(), nullable=True),
        sa.Column('weather_dependent', sa.Boolean(), nullable=True),
        sa.Column('popularity_score', sa.Float(), nullable=True),
        sa.Column('affiliate_links', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('external_id')
    )

    # Create casinos table
    op.create_table('casinos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('rating', sa.Numeric(3, 2), nullable=True),
        sa.Column('review_count', sa.Integer(), nullable=True),
        sa.Column('amenities', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('restaurants', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('shows', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('gaming_options', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('parking_info', sa.Text(), nullable=True),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('affiliate_link', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create outdoor_activities table
    op.create_table('outdoor_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('difficulty_level', sa.String(20), nullable=True),
        sa.Column('distance', sa.Float(), nullable=True),
        sa.Column('elevation_gain', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('best_seasons', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('parking_available', sa.Boolean(), nullable=True),
        sa.Column('amenities', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('tour_operators', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('affiliate_links', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create reviews table
    op.create_table('reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('casino_id', sa.Integer(), nullable=True),
        sa.Column('outdoor_activity_id', sa.Integer(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('visit_date', sa.DateTime(), nullable=True),
        sa.Column('photos', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('helpful_votes', sa.Integer(), nullable=True),
        sa.Column('verified_purchase', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['casino_id'], ['casinos.id'], ),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['outdoor_activity_id'], ['outdoor_activities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create tips table
    op.create_table('tips',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('helpful_votes', sa.Integer(), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create local_guides table
    op.create_table('local_guides',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('featured_image', sa.String(255), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('views', sa.Integer(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create photo_galleries table
    op.create_table('photo_galleries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('casino_id', sa.Integer(), nullable=True),
        sa.Column('outdoor_activity_id', sa.Integer(), nullable=True),
        sa.Column('photo_url', sa.String(255), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('taken_at', sa.DateTime(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('featured', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['casino_id'], ['casinos.id'], ),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['outdoor_activity_id'], ['outdoor_activities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create virtual_tours table
    op.create_table('virtual_tours',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('venue_name', sa.String(255), nullable=False),
        sa.Column('tour_type', sa.String(50), nullable=True),
        sa.Column('media_url', sa.String(255), nullable=False),
        sa.Column('thumbnail_url', sa.String(255), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('views', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create deals table
    op.create_table('deals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('deal_type', sa.String(50), nullable=True),
        sa.Column('venue', sa.String(255), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('terms', sa.Text(), nullable=True),
        sa.Column('promo_code', sa.String(50), nullable=True),
        sa.Column('discount_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('discount_type', sa.String(20), nullable=True),
        sa.Column('min_purchase', sa.Numeric(10, 2), nullable=True),
        sa.Column('max_discount', sa.Numeric(10, 2), nullable=True),
        sa.Column('redemption_count', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('affiliate_link', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create saved_items table
    op.create_table('saved_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create itineraries table
    op.create_table('itineraries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create itinerary_items table
    op.create_table('itinerary_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('itinerary_id', sa.Integer(), nullable=False),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create weather_forecasts table
    op.create_table('weather_forecasts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('temperature_high', sa.Float(), nullable=True),
        sa.Column('temperature_low', sa.Float(), nullable=True),
        sa.Column('conditions', sa.String(100), nullable=True),
        sa.Column('precipitation_chance', sa.Float(), nullable=True),
        sa.Column('wind_speed', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create user_preferences table
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interest', sa.String(100), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create user_interactions table
    op.create_table('user_interactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('interaction_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recommendations table
    op.create_table('recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('event_date', sa.DateTime(), nullable=True),
        sa.Column('venue', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create logs table
    op.create_table('logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('level', sa.String(50), nullable=True),
        sa.Column('source', sa.String(255), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('logs')
    op.drop_table('recommendations')
    op.drop_table('user_interactions')
    op.drop_table('user_preferences')
    op.drop_table('weather_forecasts')
    op.drop_table('itinerary_items')
    op.drop_table('itineraries')
    op.drop_table('saved_items')
    op.drop_table('deals')
    op.drop_table('virtual_tours')
    op.drop_table('photo_galleries')
    op.drop_table('local_guides')
    op.drop_table('tips')
    op.drop_table('reviews')
    op.drop_table('outdoor_activities')
    op.drop_table('casinos')
    op.drop_table('events')
    op.drop_table('affiliates')
    op.drop_table('users') 