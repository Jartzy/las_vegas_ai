// src/components/LandingPage.tsx
import React from 'react';
import EventsDisplay from './EventsDisplay';
import { Event } from '../types/event';

interface LandingPageProps {
  events: Event[];
}

const LandingPage: React.FC<LandingPageProps> = ({ events }) => {
  return (
    <>
      <section className="bg-purple-600 text-white py-16 text-center">
        <h1 className="text-5xl font-bold mb-4">Discover Amazing Events</h1>
        <p className="text-xl">Browse through concerts, sports, comedy, theatre and more.</p>
      </section>
      <main className="container mx-auto px-4 py-8">
        <EventsDisplay events={events} />
      </main>
    </>
  );
};

export default LandingPage;