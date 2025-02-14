// frontend/src/api/auth.ts

export async function login(username: string, password: string, otp: string) {
    const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, otp }),
    });
    return response.json();
}

export async function logout() {
    const response = await fetch("http://localhost:5000/api/auth/logout", {
        method: "POST",
        credentials: "include"
    });
    return response.json();
}

export async function getRecommendations() {
    const response = await fetch("http://localhost:5000/api/recommendations", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
    });
    return response.json();
}
