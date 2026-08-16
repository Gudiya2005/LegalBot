import { useState } from "react";
import {
  ShieldCheck,
  User,
  Mail,
  Lock,
  ArrowRight,
} from "lucide-react";

function Register({ onRegister, onSwitchToLogin }) {

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (e) => {

    e.preventDefault();

    setError("");

    if (!name || !email || !password) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/auth/register",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            name,
            email,
            password,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {
        throw new Error(
          data.detail || "Registration failed."
        );
      }


      onRegister();

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


        <h1>Create your account</h1>

        <p className="auth-subtitle">
          Get started with LegalBot
        </p>


        <form onSubmit={handleSubmit}>

          <label>Full Name</label>

          <div className="auth-input">

            <User size={18} />

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

          </div>


          <label>Email</label>

          <div className="auth-input">

            <Mail size={18} />

            <input
              type="email"
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
              placeholder="Create a password"
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

            {loading
              ? "Creating account..."
              : "Create Account"}

            {!loading && <ArrowRight size={18} />}

          </button>

        </form>


        <div className="auth-switch">

          Already have an account?

          <button onClick={onSwitchToLogin}>
            Sign in
          </button>

        </div>

      </div>

    </div>

  );
}

export default Register;