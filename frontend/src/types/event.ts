// src/types/event.ts
export interface Event {
  id: number;
  name: string;
  description: string | null;
  category: string | null;
  subcategory: string | null;
  price_range_min: number | null;
  price_range_max: number | null;
  venue: string | null;
  start_date: string | null;
  end_date: string | null;
  image_url: string | null;
  source: string | null;
}

export interface EventFilters {
  category: 'all' | 'music' | 'sports' | 'comedy' | 'theatre';
  priceRange:   | 'all' 
  | 'free' 
  | 'paid' 
  | 'under-50' 
  | '50-100' 
  | '100-200' 
  | 'over-200';
  timeframe: 'all' | 'today' | 'week' | 'month';
}
