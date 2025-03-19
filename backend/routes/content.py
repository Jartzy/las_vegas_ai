from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app import (
    Review, Tip, LocalGuide, PhotoGallery, VirtualTour, Deal,
    SavedItem, Itinerary, ItineraryItem, WeatherForecast
)
from sqlalchemy import desc

content = Blueprint('content', __name__)

# Reviews
@content.route('/reviews', methods=['GET'])
def get_reviews():
    item_type = request.args.get('type')  # 'event', 'casino', 'outdoor_activity'
    item_id = request.args.get('id', type=int)
    sort_by = request.args.get('sort', 'newest')  # 'newest', 'highest_rated', 'most_helpful'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Review.query
    if item_type and item_id:
        if item_type == 'event':
            query = query.filter_by(event_id=item_id)
        elif item_type == 'casino':
            query = query.filter_by(casino_id=item_id)
        elif item_type == 'outdoor_activity':
            query = query.filter_by(outdoor_activity_id=item_id)

    if sort_by == 'newest':
        query = query.order_by(desc(Review.created_at))
    elif sort_by == 'highest_rated':
        query = query.order_by(desc(Review.rating))
    elif sort_by == 'most_helpful':
        query = query.order_by(desc(Review.helpful_votes))

    reviews = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reviews': [{
            'id': r.id,
            'rating': r.rating,
            'title': r.title,
            'content': r.content,
            'visit_date': r.visit_date.isoformat() if r.visit_date else None,
            'photos': r.photos,
            'helpful_votes': r.helpful_votes,
            'verified_purchase': r.verified_purchase,
            'created_at': r.created_at.isoformat()
        } for r in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': reviews.page
    })

@content.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    review = Review(
        user_id=data['user_id'],
        event_id=data.get('event_id'),
        casino_id=data.get('casino_id'),
        outdoor_activity_id=data.get('outdoor_activity_id'),
        rating=data['rating'],
        title=data['title'],
        content=data['content'],
        visit_date=datetime.fromisoformat(data['visit_date']) if data.get('visit_date') else None,
        photos=data.get('photos', []),
        verified_purchase=data.get('verified_purchase', False)
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully', 'id': review.id}), 201

# Tips
@content.route('/tips', methods=['GET'])
def get_tips():
    category = request.args.get('category')
    tag = request.args.get('tag')
    sort_by = request.args.get('sort', 'helpful')  # 'helpful', 'newest'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Tip.query.filter_by(verified=True)
    if category:
        query = query.filter_by(category=category)
    if tag:
        query = query.filter(Tip.tags.contains([tag]))

    if sort_by == 'helpful':
        query = query.order_by(desc(Tip.helpful_votes))
    else:
        query = query.order_by(desc(Tip.created_at))

    tips = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'tips': [{
            'id': t.id,
            'category': t.category,
            'title': t.title,
            'content': t.content,
            'tags': t.tags,
            'helpful_votes': t.helpful_votes,
            'created_at': t.created_at.isoformat()
        } for t in tips.items],
        'total': tips.total,
        'pages': tips.pages,
        'current_page': tips.page
    })

# Local Guides
@content.route('/guides', methods=['GET'])
def get_guides():
    category = request.args.get('category')
    tag = request.args.get('tag')
    sort_by = request.args.get('sort', 'popular')  # 'popular', 'newest'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = LocalGuide.query
    if category:
        query = query.filter_by(category=category)
    if tag:
        query = query.filter(LocalGuide.tags.contains([tag]))

    if sort_by == 'popular':
        query = query.order_by(desc(LocalGuide.views))
    else:
        query = query.order_by(desc(LocalGuide.created_at))

    guides = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'guides': [{
            'id': g.id,
            'title': g.title,
            'content': g.content,
            'category': g.category,
            'featured_image': g.featured_image,
            'tags': g.tags,
            'views': g.views,
            'likes': g.likes,
            'created_at': g.created_at.isoformat()
        } for g in guides.items],
        'total': guides.total,
        'pages': guides.pages,
        'current_page': guides.page
    })

# Virtual Tours
@content.route('/virtual-tours', methods=['GET'])
def get_virtual_tours():
    venue = request.args.get('venue')
    tour_type = request.args.get('type')
    sort_by = request.args.get('sort', 'popular')  # 'popular', 'newest'
    
    query = VirtualTour.query
    if venue:
        query = query.filter_by(venue_name=venue)
    if tour_type:
        query = query.filter_by(tour_type=tour_type)

    if sort_by == 'popular':
        query = query.order_by(desc(VirtualTour.views))
    else:
        query = query.order_by(desc(VirtualTour.created_at))

    tours = query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'venue_name': t.venue_name,
        'tour_type': t.tour_type,
        'media_url': t.media_url,
        'thumbnail_url': t.thumbnail_url,
        'duration': t.duration,
        'views': t.views
    } for t in tours])

# Deals
@content.route('/deals', methods=['GET'])
def get_deals():
    venue = request.args.get('venue')
    deal_type = request.args.get('type')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    query = Deal.query
    if venue:
        query = query.filter_by(venue=venue)
    if deal_type:
        query = query.filter_by(deal_type=deal_type)
    if active_only:
        query = query.filter_by(active=True)
        query = query.filter(Deal.end_date >= datetime.utcnow())

    query = query.order_by(desc(Deal.created_at))
    deals = query.all()
    
    return jsonify([{
        'id': d.id,
        'title': d.title,
        'description': d.description,
        'deal_type': d.deal_type,
        'venue': d.venue,
        'start_date': d.start_date.isoformat() if d.start_date else None,
        'end_date': d.end_date.isoformat() if d.end_date else None,
        'promo_code': d.promo_code,
        'discount_amount': float(d.discount_amount),
        'discount_type': d.discount_type,
        'affiliate_link': d.affiliate_link
    } for d in deals])

# Itineraries
@content.route('/itineraries', methods=['GET'])
def get_itineraries():
    user_id = request.args.get('user_id')
    public_only = request.args.get('public_only', 'false').lower() == 'true'
    
    query = Itinerary.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if public_only:
        query = query.filter_by(is_public=True)

    query = query.order_by(desc(Itinerary.created_at))
    itineraries = query.all()
    
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'start_date': i.start_date.isoformat() if i.start_date else None,
        'end_date': i.end_date.isoformat() if i.end_date else None,
        'is_public': i.is_public,
        'likes': i.likes,
        'items': [{
            'day_number': item.day_number,
            'start_time': item.start_time.strftime('%H:%M') if item.start_time else None,
            'duration': item.duration,
            'notes': item.notes,
            'item_type': item.item_type,
            'item_id': item.item_id
        } for item in ItineraryItem.query.filter_by(itinerary_id=i.id).order_by(ItineraryItem.day_number, ItineraryItem.start_time).all()]
    } for i in itineraries])

@content.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.json
    itinerary = Itinerary(
        user_id=data['user_id'],
        title=data['title'],
        description=data.get('description'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        is_public=data.get('is_public', False)
    )
    db.session.add(itinerary)
    db.session.flush()

    for item_data in data.get('items', []):
        item = ItineraryItem(
            itinerary_id=itinerary.id,
            item_type=item_data['item_type'],
            item_id=item_data['item_id'],
            day_number=item_data['day_number'],
            start_time=datetime.strptime(item_data['start_time'], '%H:%M').time() if item_data.get('start_time') else None,
            duration=item_data.get('duration'),
            notes=item_data.get('notes')
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Itinerary created successfully', 'id': itinerary.id}), 201

# Weather
@content.route('/weather', methods=['GET'])
def get_weather():
    forecasts = WeatherForecast.query.order_by(WeatherForecast.date).all()
    return jsonify([{
        'date': f.date.isoformat(),
        'temperature_high': f.temperature_high,
        'temperature_low': f.temperature_low,
        'conditions': f.conditions,
        'precipitation_chance': f.precipitation_chance,
        'wind_speed': f.wind_speed
    } for f in forecasts])

# Saved Items
@content.route('/saved-items', methods=['GET'])
def get_saved_items():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    items = SavedItem.query.filter_by(user_id=user_id).order_by(desc(SavedItem.created_at)).all()
    return jsonify([{
        'id': item.id,
        'item_type': item.item_type,
        'item_id': item.item_id,
        'notes': item.notes,
        'created_at': item.created_at.isoformat()
    } for item in items])

@content.route('/saved-items', methods=['POST'])
def save_item():
    data = request.json
    item = SavedItem(
        user_id=data['user_id'],
        item_type=data['item_type'],
        item_id=data['item_id'],
        notes=data.get('notes')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item saved successfully', 'id': item.id}), 201

@content.route('/saved-items/<int:item_id>', methods=['DELETE'])
def remove_saved_item(item_id):
    item = SavedItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed successfully'}) 