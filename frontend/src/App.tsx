// src/App.tsx
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import EventsDisplay from './components/EventsDisplay';
import { Event } from './types/event';
import { fetchEvents } from './services/eventService';

const App: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoading(true);
        const data = await fetchEvents();
        setEvents(data);
        setError(null);
      } catch (err) {
        setError('Failed to load events. Please try again later.');
        console.error('Error loading events:', err);
      } finally {
        setLoading(false);
      }
    };
    loadEvents();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-700 to-blue-500 text-white">
      {/* Updated Header with integrated Hero */}
      <Header />

      <main className="container mx-auto px-4 py-8">
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
            <p className="mt-4 text-lg">Loading events...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-300 text-lg">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="mt-4 bg-white text-blue-900 px-4 py-2 rounded-lg hover:bg-gray-100"
            >
              Try Again
            </button>
          </div>
        ) : (
          <EventsDisplay events={events} />
        )}
      </main>
    </div>
  );
};

export default App;