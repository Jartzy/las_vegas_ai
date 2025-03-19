// src/pages/FreeCasinoShows.tsx
import React, { useEffect, useState } from 'react';
import { Event } from '../types/event';
import { fetchEvents } from '../services/eventService';
import SkeletonCard from '../components/SkeletonCard';

const FreeCasinoShows: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        // Fetch free events from backend using the priceRange filter if desired.
        // Alternatively, fetch all and filter on the client side.
        const allEvents = await fetchEvents({ category: 'all', priceRange: 'free', timeframe: 'all' });
        // Filter events where venue, name, or description includes "casino" (case-insensitive)
        const freeCasinoEvents = allEvents.filter(event => {
          const searchFields = [event.venue, event.name, event.description];
          return searchFields.some(field => field && field.toLowerCase().includes('casino'));
        });
        setEvents(freeCasinoEvents);
      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Failed to load events.');
      } finally {
        setLoading(false);
      }
    };

    loadEvents();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold mb-4">Free Casino Shows</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, idx) => (
            <SkeletonCard key={idx} />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold mb-4">Free Casino Shows</h1>
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">Free Casino Shows</h1>
      {events.length === 0 ? (
        <p>No free casino shows found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map(event => (
            <div
              key={event.id}
              className="group overflow-hidden bg-white/5 backdrop-blur-lg border border-white/10 text-white rounded-lg
                         transition-all duration-300 hover:bg-white/10 hover:scale-102 hover:shadow-xl"
            >
              {event.image_url && (
                <div className="relative h-48 w-full overflow-hidden">
                  <img
                    src={event.image_url}
                    alt={event.name}
                    className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                </div>
              )}
              <div className="p-4">
                <h3 className="text-xl font-bold mb-1 group-hover:text-purple-300 transition-colors">
                  {event.name}
                </h3>
                <p className="text-gray-300 text-sm mb-3">
                  {event.venue || 'Venue TBA'}
                </p>
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
                  {event.price_range_min === 0 ? 'FREE' : 'Paid'}
                </p>
                <p className="text-xs text-gray-400 mt-2">
                  Source: {event.source}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FreeCasinoShows;