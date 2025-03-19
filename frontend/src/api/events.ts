import { Event, EventFilters } from '../types/event';

const API_BASE_URL = '/api';

export async function getEvents(filters?: Partial<EventFilters>): Promise<Event[]> {
    // Build query parameters
    const queryParams = new URLSearchParams();
    
    if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                if (key === 'location') {
                    // Handle location object separately
                    const location = value as { latitude: number; longitude: number; radius: number };
                    queryParams.append('latitude', location.latitude.toString());
                    queryParams.append('longitude', location.longitude.toString());
                    queryParams.append('radius', location.radius.toString());
                } else if (key === 'duration') {
                    // Handle duration object
                    const duration = value as { min: number; max: number };
                    queryParams.append('duration_min', duration.min.toString());
                    queryParams.append('duration_max', duration.max.toString());
                } else if (Array.isArray(value)) {
                    // Handle array values
                    value.forEach(item => queryParams.append(key, item.toString()));
                } else {
                    // Handle simple values
                    queryParams.append(key, value.toString());
                }
            }
        });
    }

    const url = `${API_BASE_URL}/events${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch events: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
}

export async function getEventById(eventId: number): Promise<Event> {
    const url = `${API_BASE_URL}/events/${eventId}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch event: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching event:', error);
        throw error;
    }
}

export async function recordEventInteraction(
    eventId: number, 
    interactionType: 'view' | 'like' | 'dislike' | 'bookmark' | 'share'
): Promise<void> {
    const url = `${API_BASE_URL}/events/${eventId}/interact`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type: interactionType }),
        });

        if (!response.ok) {
            throw new Error(`Failed to record interaction: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error recording interaction:', error);
        throw error;
    }
} 