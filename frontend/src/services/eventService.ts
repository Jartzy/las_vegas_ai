// src/services/eventService.ts
import { useQuery } from '@tanstack/react-query';
import { Event, EventFilters } from '../types/event';

const API_BASE_URL = '/api';

export const useEvents = (filters: EventFilters) => {
  return useQuery({
    queryKey: ['events', filters],
    queryFn: async () => {
      const queryString = buildQueryString(filters);
      const url = `/api/events${queryString ? `?${queryString}` : ''}`;
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch events');
      }
      
      const data = await response.json();
      return data as Event[];
    },
  });
};

export const fetchEvent = async (eventId: number): Promise<Event> => {
  const response = await fetch(`${API_BASE_URL}/events/${eventId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch event');
  }
  return response.json();
};

export const useEvent = (eventId: number) => {
  return useQuery({
    queryKey: ['event', eventId],
    queryFn: () => fetchEvent(eventId),
    enabled: !!eventId,
  });
};

const buildQueryString = (filters: EventFilters): string => {
  const params = new URLSearchParams();
  
  if (filters.category && filters.category !== 'all') {
    params.append('category', filters.category);
  }
  
  if (filters.priceRange && filters.priceRange !== 'all') {
    params.append('priceRange', filters.priceRange);
  }
  
  if (filters.timeframe && filters.timeframe !== 'all') {
    params.append('timeframe', filters.timeframe);
  }
  
  if (filters.sortBy && filters.sortBy !== 'date') {
    params.append('sortBy', filters.sortBy);
  }
  
  if (filters.location) {
    params.append('latitude', filters.location.latitude.toString());
    params.append('longitude', filters.location.longitude.toString());
    if (filters.location.radius) {
      params.append('radius', filters.location.radius.toString());
    }
  }
  
  if (filters.rating) {
    params.append('rating', filters.rating.toString());
  }

  if (filters.dates) {
    params.append('startDate', filters.dates.start);
    params.append('endDate', filters.dates.end);
  }

  if (filters.tags?.length) {
    filters.tags.forEach(tag => params.append('tags', tag));
  }

  if (filters.venue) {
    params.append('venue', filters.venue);
  }

  if (filters.search) {
    params.append('search', filters.search);
  }
  
  return params.toString();
};