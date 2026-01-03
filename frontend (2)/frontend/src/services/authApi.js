import axios from "axios";

const baseURL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

const authClient = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

export async function loginUser(credentials) {
  try {
    const res = await authClient.post("/api/auth/login", credentials);
    return res.data;
  } catch (error) {
    console.error("Auth API error:", error);
    if (error.response) {
      const message = error.response.data?.detail || error.response.data?.message || "Authentication failed.";
      throw new Error(message);
    }
    if (error.request) {
      throw new Error("Cannot reach authentication service. Please check if the backend is running.");
    }
    throw new Error("Unexpected error during login.");
  }
}

export async function loginWithGoogle(credential) {
  try {
    const res = await authClient.post("/api/auth/google", { credential });
    return res.data;
  } catch (error) {
    console.error("Google Auth API error:", error);
    if (error.response) {
      throw new Error(error.response.data?.detail || "Google login failed.");
    }
    throw new Error("Cannot reach authentication service.");
  }
}

