// frontend/src/pages/Recommendations.tsx

import { useEffect, useState } from "react";
import { getRecommendations } from "../api/recommendations";
import AttractionCard from "../components/AttractionCard";
import Filters from "../components/Filters";

interface Recommendation {
    id: string;
    name: string;
    category: string;
}

export default function Recommendations() {
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selectedCategory, setSelectedCategory] = useState("All");

    useEffect(() => {
        async function fetchData() {
            try {
                const data: Recommendation[] = await getRecommendations();
                setRecommendations(data);
            } catch (err) {
                setError("Failed to load recommendations.");
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    const filteredRecommendations: Recommendation[] = selectedCategory === "All" 
        ? recommendations 
        : recommendations.filter((rec) => rec.category === selectedCategory);

    if (loading) return <p>Loading recommendations...</p>;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">AI-Powered Recommendations</h1>
            <Filters selectedCategory={selectedCategory} onCategoryChange={setSelectedCategory} />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredRecommendations.map((rec) => (
                    <AttractionCard key={rec.id} name={rec.name} category={rec.category} />
                ))}
            </div>
        </div>
    );
}
