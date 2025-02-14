// src/api/recommendations.ts
import { Attraction, Interest, Duration } from '../types';

interface RecommendationParams {
    interests?: Interest[];
    duration?: Duration;
    userId?: string;
}

export async function getRecommendations(params: RecommendationParams = {}) {
    // Build query parameters
    const queryParams = new URLSearchParams();
    
    if (params.interests && params.interests.length > 0) {
        params.interests.forEach(interest => {
            queryParams.append('interests', interest);
        });
    }
    
    if (params.duration) {
        queryParams.append('duration', params.duration);
    }
    
    if (params.userId) {
        queryParams.append('user_id', params.userId);
    }

    const url = `http://localhost:5000/api/recommendations?${queryParams.toString()}`;
    
    const response = await fetch(url, {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
    });
    
    if (!response.ok) {
        throw new Error("Failed to fetch recommendations");
    }
    
    const data = await response.json();
    
    // Transform the API response to match your Attraction type
    return data.map((item: any): Attraction => ({
        id: item.id,
        name: item.name,
        description: item.description || '',
        category: mapCategory(item.category),
        imageUrl: item.image_url || '/placeholder-image.jpg',
        rating: item.rating || 0,
        priceLevel: mapPriceLevel(item.price_range_max),
        location: item.venue || 'Las Vegas',
        interests: mapInterests(item.category, item.subcategory),
        duration: ['day', 'week', 'local'],
        source: 'Ticketmaster',
        isFree: item.price_range_min === 0
    }));
}

// Helper functions to map API data to your frontend types
function mapCategory(category: string): 'Entertainment' | 'Dining' | 'Nightlife' | 'Shopping' | 'Adventure' {
    const categoryMap: { [key: string]: 'Entertainment' | 'Dining' | 'Nightlife' | 'Shopping' | 'Adventure' } = {
        'Music': 'Entertainment',
        'Sports': 'Entertainment',
        'Arts & Theatre': 'Entertainment',
        'Miscellaneous': 'Entertainment',
        'Food': 'Dining',
        'Nightlife': 'Nightlife',
        'Shopping': 'Shopping',
        'Outdoor': 'Adventure'
    };
    
    return categoryMap[category] || 'Entertainment';
}

function mapPriceLevel(maxPrice?: number): '$$' | '$$$' | '$$$$' {
    if (!maxPrice) return '$$';
    if (maxPrice < 50) return '$$';
    if (maxPrice < 100) return '$$$';
    return '$$$$';
}

function mapInterests(category?: string, subcategory?: string): Interest[] {
    const interests: Interest[] = [];
    
    if (category === 'Music') interests.push('Live Music');
    if (category === 'Sports') interests.push('Sports');
    if (category === 'Arts & Theatre') interests.push('Shows');
    if (category === 'Food') interests.push('Fine Dining');
    if (category === 'Nightlife') interests.push('Nightlife');
    if (category === 'Shopping') interests.push('Shopping');
    if (category === 'Family' || subcategory === 'Family') interests.push('Family Friendly');
    
    return interests;
}

// Add interaction tracking
export async function recordInteraction(eventId: number, interactionType: 'view' | 'like' | 'dislike') {
    const response = await fetch(`http://localhost:5000/api/events/${eventId}/interact`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            type: interactionType
        })
    });
    
    if (!response.ok) {
        throw new Error('Failed to record interaction');
    }
    
    return response.json();
}