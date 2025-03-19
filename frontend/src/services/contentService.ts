import axios from 'axios';
import {
  Review, Tip, LocalGuide, VirtualTour, Deal,
  Itinerary, WeatherForecast, SavedItem, ContentFilters
} from '../types/content';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

export const contentService = {
  // Reviews
  getReviews: async (type: string, id: number, filters: ContentFilters) => {
    const response = await axios.get(`${API_BASE_URL}/content/reviews`, {
      params: { type, id, ...filters }
    });
    return response.data;
  },

  createReview: async (review: Partial<Review>) => {
    const response = await axios.post(`${API_BASE_URL}/content/reviews`, review);
    return response.data;
  },

  // Tips
  getTips: async (filters: ContentFilters) => {
    const response = await axios.get(`${API_BASE_URL}/content/tips`, {
      params: filters
    });
    return response.data;
  },

  // Local Guides
  getGuides: async (filters: ContentFilters) => {
    const response = await axios.get(`${API_BASE_URL}/content/guides`, {
      params: filters
    });
    return response.data;
  },

  // Virtual Tours
  getVirtualTours: async (venue?: string, tourType?: string) => {
    const response = await axios.get(`${API_BASE_URL}/content/virtual-tours`, {
      params: { venue, type: tourType }
    });
    return response.data as VirtualTour[];
  },

  // Deals
  getDeals: async (venue?: string, dealType?: string, activeOnly: boolean = true) => {
    const response = await axios.get(`${API_BASE_URL}/content/deals`, {
      params: { venue, type: dealType, active_only: activeOnly }
    });
    return response.data as Deal[];
  },

  // Itineraries
  getItineraries: async (userId?: string, publicOnly: boolean = false) => {
    const response = await axios.get(`${API_BASE_URL}/content/itineraries`, {
      params: { user_id: userId, public_only: publicOnly }
    });
    return response.data as Itinerary[];
  },

  createItinerary: async (itinerary: Partial<Itinerary>) => {
    const response = await axios.post(`${API_BASE_URL}/content/itineraries`, itinerary);
    return response.data;
  },

  // Weather
  getWeatherForecast: async () => {
    const response = await axios.get(`${API_BASE_URL}/content/weather`);
    return response.data as WeatherForecast[];
  },

  // Saved Items
  getSavedItems: async (userId: string) => {
    const response = await axios.get(`${API_BASE_URL}/content/saved-items`, {
      params: { user_id: userId }
    });
    return response.data as SavedItem[];
  },

  saveItem: async (item: Partial<SavedItem>) => {
    const response = await axios.post(`${API_BASE_URL}/content/saved-items`, item);
    return response.data;
  },

  removeSavedItem: async (itemId: number) => {
    const response = await axios.delete(`${API_BASE_URL}/content/saved-items/${itemId}`);
    return response.data;
  }
}; 