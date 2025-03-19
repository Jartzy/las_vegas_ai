import React from 'react';

// A very simple component with no dependencies
const SimpleApp: React.FC = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Las Vegas Activities</h1>
      <p>This is a simplified version of the app to help debug issues.</p>
      <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <h2>Local Guides</h2>
        <p>Discover the best of Las Vegas with our curated guides.</p>
      </div>
      <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <h2>Deals & Offers</h2>
        <p>Find the best deals on shows, dining, and attractions.</p>
      </div>
      <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <h2>Reviews</h2>
        <p>Read reviews from other visitors to plan your perfect trip.</p>
      </div>
    </div>
  );
};

export default SimpleApp; 