// src/components/Header.tsx
import React from 'react';
import { Brain } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="relative bg-gradient-to-r from-blue-900 via-blue-700 to-blue-500 text-white">
      {/* Top Nav */}
      <div className="container mx-auto flex items-center justify-between py-4 px-4">
        <div className="flex items-center space-x-2">
          <Brain className="w-8 h-8" />
          <span className="font-bold text-xl">Las VAIgas</span>
        </div>
        <nav className="space-x-6 hidden md:block">
          <a href="#" className="hover:text-gray-300 transition-colors">All Recommendations</a>
          <a href="#" className="hover:text-gray-300 transition-colors">Attractions</a>
          <a href="#" className="hover:text-gray-300 transition-colors">About</a>
        </nav>
      </div>

      {/* Hero Section */}
      <div className="bg-purple-600 py-12 md:py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Discover Amazing Events</h1>
        <p className="text-xl text-gray-100 max-w-xl mx-auto">
          Browse through concerts, sports, comedy, theatre and more.
        </p>
      </div>
    </header>
  );
};

export default Header;