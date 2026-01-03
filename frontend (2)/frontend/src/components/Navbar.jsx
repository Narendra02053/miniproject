import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const linkClass = ({ isActive }) =>
    `navbar__link${isActive ? " navbar__link--active" : ""}`;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="navbar">
      <div className="navbar__brand">
        <span role="img" aria-hidden="true">
          🧠
        </span>{" "}
        Memory Companion
      </div>
      <nav className="navbar__links">
        {user && (
          <>
            <NavLink to="/" className={linkClass} end>
              Predict
            </NavLink>
            <NavLink to="/chat" className={linkClass}>
              Chatbot
            </NavLink>
          </>
        )}
        {!user && (
          <NavLink to="/login" className={linkClass}>
            Login
          </NavLink>
        )}
      </nav>
      {user && (
        <div className="navbar__user">
          <span className="navbar__email">{user.email}</span>
          <button className="btn btn--ghost btn--tiny" onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </header>
  );
}
