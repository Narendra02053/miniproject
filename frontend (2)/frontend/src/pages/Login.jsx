import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { loginUser, loginWithGoogle } from "../services/authApi";
import { GoogleLogin } from "@react-oauth/google";

const initialState = { email: "", password: "" };

// Horror Audio Synthesizer


export default function Login() {
  const [form, setForm] = useState(initialState);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [showVecna, setShowVecna] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const triggerAnimation = () => {
    // 1. Start Animation
    setShowVecna(true);

    // 2. Play Sound (Removed as per user request)
    // playVecnaSound();

    // 3. Shake Screen
    document.body.classList.add("shake-screen");
    setTimeout(() => document.body.classList.remove("shake-screen"), 600);

    // 4. Return promise that resolves when animation matches
    return new Promise((resolve) => setTimeout(resolve, 5800)); // Match the CSS animation duration (1.5s delay + 4s walk + buffer)
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (status === "loading" || showVecna) return;

    setStatus("loading");
    setError("");

    try {
      // 1. Verify credentials first
      const response = await loginUser(form);

      // 2. If success, trigger animation
      if (response?.user) {
        await triggerAnimation();

        // 3. After animation, effectively login and redirect
        login(response.user);
        navigate("/", { replace: true });
      } else {
        throw new Error("Invalid response from auth service.");
      }
    } catch (err) {
      console.error("Login failed:", err);
      // Even on failure, for the "experience", we could optionally scare them, 
      // but let's keep it to success for now so they don't get scared away from retrying.
      setError(err.message || "Login failed. Please try again.");
      setStatus("idle");
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    if (status === "loading" || showVecna) return;

    setStatus("loading");
    setError("");

    try {
      const response = await loginWithGoogle(credentialResponse.credential);

      if (response?.user) {
        await triggerAnimation();
        login(response.user);
        navigate("/", { replace: true });
      } else {
        throw new Error("Invalid response from Google auth.");
      }
    } catch (err) {
      console.error("Google Login failed:", err);
      setError(err.message || "Google Login failed.");
      setStatus("idle");
    }
  };

  return (
    <main className="page">
      {/* Vecna Animation Overlay */}
      {showVecna && (
        <div className="vecna-overlay">
          <img
            src="/vecna_transparent.png"
            alt="Vecna"
            className="vecna-sprite animate-jump-scare"
          />
        </div>
      )}

      {!showVecna && (
        <div className="page-header">
          <h1>Welcome back</h1>
          <p>Sign in to see your saved predictions and chat history.</p>
        </div>
      )}

      {!showVecna && (
        <section className="card login-card">
          <form className="form-grid" onSubmit={handleSubmit}>

            <div className="google-login-container" style={{ gridColumn: "1 / -1", display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => {
                  setError("Google Login Failed");
                }}
                theme="filled_black"
                shape="pill"
              />
            </div>

            <div className="divider" style={{ gridColumn: "1 / -1", textAlign: "center", margin: "10px 0", color: "#666" }}>
              <span>OR</span>
            </div>

            <div className="input-group" style={{ gridColumn: "1 / -1" }}>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                className="input"
                placeholder="you@example.com"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="input-group" style={{ gridColumn: "1 / -1" }}>
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                className="input"
                placeholder="Enter a secure password"
                value={form.password}
                onChange={handleChange}
                minLength={6}
                required
              />
              <span className="status-text">
                First time here? We'll create your account after you pick a password.
              </span>
            </div>

            {error && (
              <p className="status-text status-text--error" style={{ gridColumn: "1 / -1" }}>
                {error}
              </p>
            )}

            <div className="toolbar" style={{ justifyContent: "flex-end", width: "100%" }}>
              <button className="btn" type="submit" disabled={status === "loading" || showVecna}>
                {status === "loading" ? (
                  <>
                    <span className="loading"></span>
                    {showVecna ? "RUN!" : "Signing in..."}
                  </>
                ) : (
                  "🔐 Continue"
                )}
              </button>
            </div>
          </form>
        </section>
      )}
    </main>
  );
}

