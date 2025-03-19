// src/pages/Restaurants.tsx
import React, { useState, useEffect } from 'react';

interface Restaurant {
  place_id: string;
  name: string;
  formatted_address: string;
  rating?: number;
  // If you have photos, you might include a photo_reference
  photo_reference?: string;
}

const Restaurants: React.FC = () => {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/restaurants', {
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch restaurants');
        }
        const data: Restaurant[] = await response.json();
        setRestaurants(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Failed to load restaurants.');
      } finally {
        setLoading(false);
      }
    };

    fetchRestaurants();
  }, []);

  if (loading) return <div>Loading restaurants...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Restaurants in Las Vegas</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {restaurants.map((restaurant) => (
          <div key={restaurant.place_id} className="bg-white/5 p-4 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-2">{restaurant.name}</h2>
            <p className="text-sm mb-2">{restaurant.formatted_address}</p>
            {restaurant.rating && <p className="text-sm">Rating: {restaurant.rating}</p>}
            {/* If you wish to display a photo, you can construct a URL from photo_reference */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Restaurants;