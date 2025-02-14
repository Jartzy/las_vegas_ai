// src/components/EventsDisplay.tsx
import React, { useState, useEffect } from 'react';
import { Event, EventFilters as FiltersInterface } from '../types/event';
import { Filter } from 'lucide-react';
import SkeletonCard from './SkeletonCard';

interface EventsDisplayProps {
  events: Event[];
}

type PriceRange = 'all' | 'free' | 'under-50' | '50-100' | '100-200' | 'over-200';
type Timeframe = 'all' | 'today' | 'week' | 'month';
type Category = 'all' | 'music' | 'sports' | 'comedy' | 'theatre';

const EventsDisplay: React.FC<EventsDisplayProps> = ({ events }) => {
  const [filters, setFilters] = useState<FiltersInterface>({
    category: 'all',
    priceRange: 'all',
    timeframe: 'all'
  });
  const [filteredEvents, setFilteredEvents] = useState<Event[]>(events);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Simulate loading state
  useEffect(() => {
    // Simulate a delay (e.g., fetching data)
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, [events]);

  useEffect(() => {
    let newFilteredEvents = events;

    if (filters.category !== 'all') {
      newFilteredEvents = newFilteredEvents.filter(
        event => event.category === filters.category
      );
    }

    if (filters.priceRange !== 'all') {
      switch (filters.priceRange) {
        case 'free':
          newFilteredEvents = newFilteredEvents.filter(
            event => event.price_range_min === 0 || event.price_range_max === 0
          );
          break;
        case 'under-50':
          newFilteredEvents = newFilteredEvents.filter(
            event =>
              event.price_range_min !== null &&
              event.price_range_min > 0 &&
              event.price_range_min < 50
          );
          break;
        case '50-100':
          newFilteredEvents = newFilteredEvents.filter(
            event =>
              event.price_range_min !== null &&
              event.price_range_min >= 50 &&
              event.price_range_min <= 100
          );
          break;
        case '100-200':
          newFilteredEvents = newFilteredEvents.filter(
            event =>
              event.price_range_min !== null &&
              event.price_range_min > 100 &&
              event.price_range_min <= 200
          );
          break;
        case 'over-200':
          newFilteredEvents = newFilteredEvents.filter(
            event =>
              event.price_range_min !== null &&
              event.price_range_min > 200
          );
          break;
      }
    }

    if (filters.timeframe !== 'all') {
      const now = new Date();
      if (filters.timeframe === 'today') {
        newFilteredEvents = newFilteredEvents.filter(event => {
          if (event.start_date) {
            const eventDate = new Date(event.start_date);
            return eventDate.toDateString() === now.toDateString();
          }
          return false;
        });
      } else if (filters.timeframe === 'week') {
        const weekFromNow = new Date();
        weekFromNow.setDate(now.getDate() + 7);
        newFilteredEvents = newFilteredEvents.filter(event => {
          if (event.start_date) {
            const eventDate = new Date(event.start_date);
            return eventDate >= now && eventDate <= weekFromNow;
          }
          return false;
        });
      }
    }

    setFilteredEvents(newFilteredEvents);
  }, [filters, events]);

  const formatPrice = (min: number | null, max: number | null) => {
    if (min === null && max === null) return 'Price not available';
    if (min === 0 && max === 0) return 'Free';
    if (min === null) return `Up to $${max?.toLocaleString()}`;
    if (max === null) return `From $${min.toLocaleString()}`;
    if (min === max) return `$${min.toLocaleString()}`;
    return `$${min.toLocaleString()} - $${max.toLocaleString()}`;
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Filter Bar */}
      <div className="bg-white/5 backdrop-blur-lg rounded-xl p-4 mb-8 shadow-lg flex items-center space-x-4">
        <div className="flex items-center text-purple-400">
          <Filter className="w-5 h-5" />
        </div>
        <div className="flex-grow grid grid-cols-3 gap-4">
          <select 
            className="w-full bg-white/10 text-white p-2 rounded-lg border border-white/20"
            value={filters.category}
            onChange={(e) => setFilters(prev => ({ 
              ...prev, 
              category: e.target.value as Category 
            }))}
          >
            <option value="all">All Categories</option>
            <option value="music">Music</option>
            <option value="sports">Sports</option>
            <option value="comedy">Comedy</option>
            <option value="theatre">Theatre</option>
          </select>
          <select 
            className="w-full bg-white/10 text-white p-2 rounded-lg border border-white/20"
            value={filters.priceRange}
            onChange={(e) => setFilters(prev => ({ 
              ...prev, 
              priceRange: e.target.value as PriceRange 
            }))}
          >
            <option value="all">All Prices</option>
            <option value="free">Free Events</option>
            <option value="under-50">Under $50</option>
            <option value="50-100">$50 - $100</option>
            <option value="100-200">$100 - $200</option>
            <option value="over-200">$200+</option>
          </select>
          <select 
            className="w-full bg-white/10 text-white p-2 rounded-lg border border-white/20"
            value={filters.timeframe}
            onChange={(e) => setFilters(prev => ({ 
              ...prev, 
              timeframe: e.target.value as Timeframe 
            }))}
          >
            <option value="all">Any Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          // Render 6 skeletons during loading
          Array.from({ length: 6 }).map((_, idx) => (
            <SkeletonCard key={idx} />
          ))
        ) : (
          filteredEvents.map(event => (
            <div 
              key={event.id} 
              className="group overflow-hidden bg-white/5 backdrop-blur-lg border border-white/10 text-white rounded-lg
                        transition-all duration-300 hover:bg-white/10 hover:scale-102 hover:shadow-xl"
            >
              <div className="relative">
                {event.image_url && (
                  <div className="relative h-48 w-full overflow-hidden">
                    <img 
                      src={event.image_url} 
                      alt={event.name}
                      className="absolute inset-0 w-full h-full object-cover
                                transition-transform duration-300 group-hover:scale-110"
                    />
                    {/* Price Badge */}
                    <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm px-3 py-1 rounded-full
                                  text-sm font-semibold text-white">
                      {event.price_range_min === 0 ? 'FREE' : 
                       `From $${event.price_range_min?.toLocaleString()}`}
                    </div>
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="text-xl font-bold mb-1 group-hover:text-purple-300 transition-colors">
                  {event.name}
                </h3>
                <p className="text-gray-300 text-sm mb-3">
                  {event.venue || 'Venue TBA'}
                </p>
                <div className="space-y-2">
                  {event.start_date && (
                    <p className="text-sm">
                      {new Date(event.start_date).toLocaleDateString(undefined, {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </p>
                  )}
                  <p className="text-sm font-medium">
                    {formatPrice(event.price_range_min, event.price_range_max)}
                  </p>
                  {event.description && (
                    <p className="text-sm text-gray-300 line-clamp-2">
                      {event.description}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventsDisplay;