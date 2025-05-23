import { useState } from "react";

export default function EmailConfirmation() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Basic regex for Gmail validation (case insensitive)
  const isValidGmail = (email: string) => {
    return /^[a-zA-Z0-9._%+-]+@gmail\.com$/i.test(email.trim());
  };

  const sendConfirmation = async () => {
    if (!isValidGmail(email)) {
      setMessage("Please enter a valid Gmail address.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("/send-confirmation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      if (res.ok) {
        setMessage("✅ Confirmation email sent! Check your inbox.");
      } else {
        setMessage("❌ Failed to send confirmation email.");
      }
    } catch (error) {
      setMessage("⚠️ Error sending confirmation email.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-gray-800 rounded text-white max-w-md mx-auto mt-6">
      <label htmlFor="email" className="mb-2 block font-bold text-lg">
        Enter your Gmail to get confirmation email:
      </label>
      <input
        id="email"
        type="email"
        placeholder="yourname@gmail.com"
        className="w-full p-2 rounded text-black"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={loading}
      />
      <button
        onClick={sendConfirmation}
        disabled={loading}
        className={`mt-2 px-4 py-2 rounded ${
          loading ? "bg-green-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {loading ? "Sending..." : "Send Confirmation Email"}
      </button>
      {message && <p className="mt-2">{message}</p>}
    </div>
  );
}
