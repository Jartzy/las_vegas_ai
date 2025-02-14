// frontend/src/api/recommendations.ts

export async function getRecommendations() {
    const response = await fetch("http://localhost:5000/api/recommendations", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
    });
    
    if (!response.ok) {
        throw new Error("Failed to fetch recommendations");
    }
    
    return response.json();
}
