import { useState } from "react";
import { ShieldCheck, Mail, Lock, ArrowRight } from "lucide-react";

function Login({ onLogin, onSwitchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed.");
      }

      localStorage.setItem("token", data.access_token);

      onLogin(
        data.access_token,
        email,
        password
      );

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          <ShieldCheck size={30} />
        </div>

        <h1>Welcome back</h1>

        <p className="auth-subtitle">
          Sign in to continue using LegalBot
        </p>

        <form onSubmit={handleSubmit} autoComplete="on">
          <label>Email</label>

          <div className="auth-input">

            <Mail size={18} />

            <input
              type="email"
              name="email"
              autoComplete="username"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

          </div>


          <label>Password</label>

          <div className="auth-input">

            <Lock size={18} />

            <input
              type="password"
              name="password"
              autoComplete="current-password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

          </div>


          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}


          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}

            {!loading && <ArrowRight size={18} />}
          </button>

        </form>


        <div className="auth-switch">

          Don't have an account?

          <button onClick={onSwitchToRegister}>
            Create one
          </button>

        </div>

      </div>

    </div>
  );
}

export default Login;