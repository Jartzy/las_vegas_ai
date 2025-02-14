// src/components/SkeletonCard.tsx
import React from 'react';

const SkeletonCard: React.FC = () => {
  return (
    <div className="group overflow-hidden bg-white/5 backdrop-blur-lg border border-white/10 text-white rounded-lg animate-pulse">
      <div className="relative">
        <div className="h-48 w-full bg-gray-700"></div>
        {/* Simulated Price Badge */}
        <div className="absolute top-4 right-4 bg-gray-600 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-semibold text-white">
          &nbsp;
        </div>
      </div>
      <div className="p-4 space-y-2">
        <div className="h-6 bg-gray-700 rounded w-3/4"></div>
        <div className="h-4 bg-gray-700 rounded w-1/2"></div>
        <div className="space-y-1">
          <div className="h-4 bg-gray-700 rounded w-full"></div>
          <div className="h-4 bg-gray-700 rounded w-5/6"></div>
          <div className="h-4 bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  );
};

export default SkeletonCard;