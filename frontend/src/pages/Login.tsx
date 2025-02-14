// frontend/src/pages/Login.tsx

import { useState } from "react";
import { login } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [otp, setOtp] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        const response = await login(username, password, otp);
        if (response.success) {
            navigate("/recommendations");
        } else {
            setError(response.message);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-2xl font-bold mb-4">Login</h1>
            <form onSubmit={handleLogin} className="flex flex-col gap-3">
                <input type="text" placeholder="Username" value={username} 
                    onChange={(e) => setUsername(e.target.value)} className="border p-2" required />
                <input type="password" placeholder="Password" value={password} 
                    onChange={(e) => setPassword(e.target.value)} className="border p-2" required />
                <input type="text" placeholder="2FA Code" value={otp} 
                    onChange={(e) => setOtp(e.target.value)} className="border p-2" required />
                <button type="submit" className="bg-blue-500 text-white p-2">Login</button>
            </form>
            {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>
    );
}
