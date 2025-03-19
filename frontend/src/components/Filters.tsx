// src/components/Filters.tsx
import React from 'react';

interface FiltersProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const Filters: React.FC<FiltersProps> = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="mb-4">
      <label htmlFor="category-filter" className="mr-2 font-medium">
        Filter by Category:
      </label>
      <select
        id="category-filter"
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="p-2 rounded border border-gray-300"
      >
        <option value="All">All</option>
        <option value="Music">Music</option>
        <option value="Sports">Sports</option>
        <option value="Comedy">Comedy</option>
        <option value="Theatre">Theatre</option>
      </select>
    </div>
  );
};

export default Filters;