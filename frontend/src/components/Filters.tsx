// frontend/src/components/Filters.tsx

interface FiltersProps {
    selectedCategory: string;
    onCategoryChange: (category: string) => void;
}

export default function Filters({ selectedCategory, onCategoryChange }: FiltersProps) {
    const categories = ["All", "Food & Drink", "Nightlife", "Outdoor & Adventure", "Events", "Hidden Gems"];

}
