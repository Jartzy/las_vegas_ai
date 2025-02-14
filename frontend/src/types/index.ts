// src/types/index.ts
export interface Attraction {
    id: number;
    name: string;
    description: string;
    category: 'Entertainment' | 'Dining' | 'Nightlife' | 'Shopping' | 'Adventure';
    imageUrl: string;
    rating: number;
    priceLevel: '$$' | '$$$' | '$$$$';
    location: string;
    interests: Interest[];
    duration: Duration[];
    source?: string;
    isFree?: boolean;
  }
  
  export interface Recommendation {
    title: string;
    description: string;
    attractions: Attraction[];
    duration: Duration;
  }
  
  export type Duration = 'day' | 'week' | 'local';
  
  export type Interest = 
    | 'Gambling'
    | 'Live Music'
    | 'Outdoors'
    | 'Fine Dining'
    | 'Shows'
    | 'Shopping'
    | 'Nightlife'
    | 'Family Friendly'
    | 'Sports';
  
  export type Purpose = 
    | 'Business'
    | 'Bachelor/Bachelorette'
    | 'Family Vacation'
    | 'Romantic Getaway'
    | 'Solo Adventure'
    | 'Friends Trip';