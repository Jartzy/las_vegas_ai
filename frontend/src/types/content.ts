export interface Review {
  id: number;
  user_id: string;
  rating: number;
  title: string;
  content: string;
  visit_date?: string;
  photos: string[];
  helpful_votes: number;
  verified_purchase: boolean;
  created_at: string;
}

export interface ReviewResponse {
  reviews: Review[];
  total: number;
  pages: number;
  current_page: number;
}

export interface Tip {
  id: number;
  category: string;
  title: string;
  content: string;
  tags: string[];
  helpful_votes: number;
  created_at: string;
}

export interface LocalGuide {
  id: number;
  title: string;
  content: string;
  category: string;
  featured_image: string;
  tags: string[];
  views: number;
  likes: number;
  created_at: string;
}

export interface VirtualTour {
  id: number;
  title: string;
  description: string;
  venue_name: string;
  tour_type: '360' | 'video' | 'interactive';
  media_url: string;
  thumbnail_url: string;
  duration: number;
  views: number;
}

export interface Deal {
  id: number;
  title: string;
  description: string;
  deal_type: 'discount' | 'package' | 'special_offer';
  venue: string;
  start_date?: string;
  end_date?: string;
  promo_code: string;
  discount_amount: number;
  discount_type: 'percentage' | 'fixed';
  affiliate_link: string;
}

export interface Itinerary {
  id: number;
  title: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_public: boolean;
  likes: number;
  items: ItineraryItem[];
}

export interface ItineraryItem {
  day_number: number;
  start_time?: string;
  duration?: number;
  notes?: string;
  item_type: 'event' | 'casino' | 'outdoor_activity';
  item_id: number;
}

export interface WeatherForecast {
  date: string;
  temperature_high: number;
  temperature_low: number;
  conditions: string;
  precipitation_chance: number;
  wind_speed: number;
}

export interface SavedItem {
  id: number;
  user_id: string;
  item_type: 'event' | 'casino' | 'outdoor_activity' | 'deal';
  item_id: number;
  notes?: string;
  created_at: string;
}

export interface ContentFilters {
  category?: string;
  tag?: string;
  venue?: string;
  sort?: 'newest' | 'popular' | 'highest_rated' | 'most_helpful';
  page?: number;
  per_page?: number;
}

export interface GuideResponse {
  guides: LocalGuide[];
  total: number;
  pages: number;
  current_page: number;
} 