// frontend/src/components/Filters.tsx

interface FiltersProps {
    selectedCategory: string;
    onCategoryChange: (category: string) => void;
}

export default function Filters({ selectedCategory, onCategoryChange }: FiltersProps) {
    const categories = ["All", "Food & Drink", "Nightlife", "Outdoor & Adventure", "Events", "Hidden Gems"];

    return (
        <div className="flex gap-4 mb-4">
            {categories.map((category) => (
                <button
                    key={category}
                    className={`px-4 py-2 rounded-md border ${selectedCategory === category ? "bg-blue-500 text-white" : "bg-gray-200"}`}
                    onClick={() => onCategoryChange(category)}
                >
                    {category}
                </button>
            ))}
        </div>
    );
}
