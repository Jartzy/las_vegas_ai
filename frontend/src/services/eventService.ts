// src/services/eventService.ts
import { Event, EventFilters } from '../types/event';

export const fetchEvents = async (filters?: EventFilters): Promise<Event[]> => {
  try {
    // In production, this would be an API call to your backend
    const response = await fetch('http://localhost:5001/api/events');
    if (!response.ok) {
      throw new Error('Failed to fetch events');
    }
    
    const events: Event[] = await response.json();
    
    // Apply filters if they exist
    if (filters) {
      return events.filter(event => {
        // Category filter
        if (filters.category !== 'all' && event.category) {
          if (event.category.toLowerCase() !== filters.category.toLowerCase()) {
            return false;
          }
        }

        // Price range filter
        if (filters.priceRange !== 'all') {
          if (filters.priceRange === 'free') {
            if (event.price_range_min !== 0 || event.price_range_min === null) {
              return false;
            }
          } else if (filters.priceRange === 'paid') {
            if (event.price_range_min === 0 || event.price_range_min === null) {
              return false;
            }
          }
        }

        // Timeframe filter
        if (filters.timeframe !== 'all' && event.start_date) {
          const eventDate = new Date(event.start_date);
          const today = new Date();
          
          switch (filters.timeframe) {
            case 'today':
              if (eventDate.toDateString() !== today.toDateString()) {
                return false;
              }
              break;
            case 'week':
              const weekFromNow = new Date();
              weekFromNow.setDate(today.getDate() + 7);
              if (eventDate > weekFromNow || eventDate < today) {
                return false;
              }
              break;
            case 'month':
              const monthFromNow = new Date();
              monthFromNow.setMonth(today.getMonth() + 1);
              if (eventDate > monthFromNow || eventDate < today) {
                return false;
              }
              break;
          }
        }

        return true;
      });
    }

    return events;
  } catch (error) {
    console.error('Error fetching events:', error);
    throw new Error('Failed to fetch events');
  }
};