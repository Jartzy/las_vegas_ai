from flask import Blueprint, jsonify, request, render_template
from database import get_db_connection
import psycopg2.extras
from datetime import datetime, timedelta
from flask_cors import cross_origin
from sqlalchemy import func
from models import Event, db

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/api/recommendations', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_recommendations():
    """API endpoint for fetching recommendations."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Get query parameters
        user_id = request.args.get('user_id')
        interests = request.args.getlist('interests')
        duration = request.args.get('duration')

        # Base query
        query = """
            SELECT 
                e.id,
                e.name,
                e.description,
                e.category,
                e.subcategory,
                e.price_range_min,
                e.price_range_max,
                e.venue,
                e.start_date,
                e.end_date,
                e.image_url,
                e.rating
            FROM events e
            WHERE e.start_date >= CURRENT_DATE
        """
        
        params = []
        
        # Add filters based on parameters
        if interests:
            query += " AND e.category = ANY(%s)"
            params.append(interests)
            
        if duration == 'day':
            query += " AND e.start_date <= CURRENT_DATE + INTERVAL '1 day'"
        elif duration == 'week':
            query += " AND e.start_date <= CURRENT_DATE + INTERVAL '7 days'"
            
        # Add ordering
        query += " ORDER BY e.start_date ASC LIMIT 20"
        
        cur.execute(query, params)
        recommendations = []
        
        for row in cur.fetchall():
            # Convert datetime objects to strings for JSON serialization
            event = dict(row)
            if event['start_date']:
                event['start_date'] = event['start_date'].isoformat()
            if event['end_date']:
                event['end_date'] = event['end_date'].isoformat()
                
            recommendations.append(event)

        cur.close()
        conn.close()
        
        return jsonify(recommendations)
        
    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@recommendations_bp.route('/recommendations', methods=['GET'])
def recommendations_page():
    """HTML page for viewing recommendations."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
            SELECT * FROM events 
            WHERE start_date >= CURRENT_DATE 
            ORDER BY start_date ASC 
            LIMIT 50
        """)
        
        recommendations = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('recommendations.html', recommendations=recommendations)
        
    except Exception as e:
        print(f"Error rendering recommendations page: {str(e)}")
        return "An error occurred", 500

bp = Blueprint('api', __name__)

@bp.route('/events', methods=['GET'])
def get_events():
    # Get query parameters
    category = request.args.get('category', 'all')
    price_range = request.args.get('priceRange', 'all')
    timeframe = request.args.get('timeframe', 'all')
    sort_by = request.args.get('sortBy', 'date')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 10, type=float)  # Default 10 miles

    # Start with base query
    query = Event.query.filter(Event.start_date >= datetime.utcnow())

    # Apply category filter
    if category != 'all':
        query = query.filter(Event.category == category)

    # Apply price range filter
    if price_range == 'under-50':
        query = query.filter(Event.price_range_min < 50)
    elif price_range == '50-100':
        query = query.filter(Event.price_range_min >= 50, Event.price_range_min < 100)
    elif price_range == '100-200':
        query = query.filter(Event.price_range_min >= 100, Event.price_range_min < 200)
    elif price_range == 'over-200':
        query = query.filter(Event.price_range_min >= 200)

    # Apply timeframe filter
    now = datetime.utcnow()
    if timeframe == 'today':
        query = query.filter(func.date(Event.start_date) == func.date(now))
    elif timeframe == 'this-week':
        query = query.filter(
            Event.start_date >= now,
            Event.start_date <= now + timedelta(days=7)
        )
    elif timeframe == 'this-month':
        query = query.filter(
            Event.start_date >= now,
            Event.start_date <= now + timedelta(days=30)
        )

    # Apply location filter if coordinates are provided
    if lat is not None and lng is not None:
        # Haversine formula for calculating distance
        radius_miles = radius
        radius_km = radius_miles * 1.60934  # Convert miles to kilometers
        earth_radius_km = 6371

        # Calculate bounding box for initial filtering
        lat_range = radius_km / earth_radius_km * (180 / 3.14159)
        lng_range = lat_range / func.cos(func.radians(lat))

        query = query.filter(
            Event.latitude.between(lat - lat_range, lat + lat_range),
            Event.longitude.between(lng - lng_range, lng + lng_range)
        )

        # Calculate exact distances and filter
        distance = (
            func.acos(
                func.least(1.0,
                    func.cos(func.radians(lat)) *
                    func.cos(func.radians(Event.latitude)) *
                    func.cos(func.radians(Event.longitude - lng)) +
                    func.sin(func.radians(lat)) *
                    func.sin(func.radians(Event.latitude))
                )
            ) * earth_radius_km
        )

        query = query.having(distance <= radius_km)

    # Apply sorting
    if sort_by == 'date':
        query = query.order_by(Event.start_date)
    elif sort_by == 'price-low':
        query = query.order_by(Event.price_range_min)
    elif sort_by == 'price-high':
        query = query.order_by(Event.price_range_min.desc())
    elif sort_by == 'rating':
        query = query.order_by(Event.rating.desc())

    # Execute query and format results
    events = query.all()
    return jsonify([{
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'start_date': event.start_date.isoformat(),
        'end_date': event.end_date.isoformat() if event.end_date else None,
        'image_url': event.image_url,
        'category': event.category,
        'price_range_min': event.price_range_min,
        'price_range_max': event.price_range_max,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'address': event.address,
        'rating': event.rating,
        'review_count': event.review_count,
        'source': event.source,
        'tags': event.tags
    } for event in events])

@bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'long_description': event.long_description,
        'start_date': event.start_date.isoformat(),
        'end_date': event.end_date.isoformat() if event.end_date else None,
        'image_url': event.image_url,
        'gallery_images': event.gallery_images,
        'category': event.category,
        'subcategory': event.subcategory,
        'price_range_min': event.price_range_min,
        'price_range_max': event.price_range_max,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'address': event.address,
        'rating': event.rating,
        'review_count': event.review_count,
        'source': event.source,
        'tags': event.tags,
        'venue': {
            'name': event.venue_name,
            'address': event.address,
            'city': 'Las Vegas',
            'state': 'NV',
            'zip': '89109'
        },
        'duration_minutes': event.duration_minutes,
        'capacity': event.capacity,
        'availability': event.availability,
        'age_restriction': event.age_restriction,
        'parking_info': event.parking_info,
        'accessibility_options': event.accessibility_options,
        'language': event.language,
        'health_safety_measures': event.health_safety_measures,
        'cancellation_policy': event.cancellation_policy,
        'booking_url': event.booking_url,
        'reviews': event.reviews or []
    })