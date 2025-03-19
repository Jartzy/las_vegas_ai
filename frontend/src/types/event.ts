export interface Event {
  id: number;
  name: string;
  description: string;
  long_description?: string;
  image_url: string;
  gallery_images?: string[];
  category: string;
  subcategory?: string;
  tags?: string[];
  price_range_min: number;
  price_range_max?: number;
  rating: number;
  review_count: number;
  reviews?: Review[];
  start_date: string;
  end_date: string;
  address: string;
  latitude: number;
  longitude: number;
  source: string;
  booking_url?: string;
  url?: string;
  affiliate_links?: {
    tickets?: string;
    [key: string]: string | undefined;
  };
  amenities?: string[];
  health_safety_measures?: string[];
  accessibility_options?: string[];
  age_restriction?: number | string;
  parking_info?: string;
  language?: string;
  dress_code?: string;
  duration_minutes?: number;
  capacity?: number;
  availability?: number;
  cancellation_policy?: string;
  venue?: {
    name: string;
    address: string;
    city: string;
    state: string;
    zip: string;
  };
}

export interface Review {
  id: number;
  user_name: string;
  rating: number;
  comment: string;
  date: string;
  images?: string[];
}

export type EventCategory =
  | 'shows'
  | 'concerts'
  | 'sports'
  | 'comedy'
  | 'cirque'
  | 'magic'
  | 'food'
  | 'nightlife'
  | 'attractions'
  | 'outdoor'
  | 'family'
  | 'shopping'
  | 'spa'
  | 'gaming'
  | 'all';

export type EventSource = 
  | 'ticketmaster'
  | 'eventbrite'
  | 'vegas'
  | 'internal';

export interface EventFilters {
  category?: EventCategory;
  priceRange?: string;
  timeframe?: string;
  sortBy?: string;
  location?: { 
    latitude: number; 
    longitude: number;
    radius?: number;
  };
  rating?: number;
  dates?: {
    start: string;
    end: string;
  };
  tags?: string[];
  venue?: string;
  search?: string;
}