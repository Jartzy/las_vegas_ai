from flask import Blueprint, jsonify, request, render_template
from database import get_db_connection
import psycopg2.extras
from datetime import datetime
from flask_cors import cross_origin

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