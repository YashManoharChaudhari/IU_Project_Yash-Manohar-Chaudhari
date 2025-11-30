import React, { useState } from "react";
import Header from "./components/Header";
import ResumeForm from "./components/ResumeForm";
import Result from "./components/Result";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  return (
    <div className="app-root">
      <Header />
      <main className="main-container">
        <div className="glass-card">
          <ResumeForm setResult={setResult} setError={setError} />
          {error && <div className="error-pill">{error}</div>}
          {result && <Result result={result} />}
        </div>
      </main>
    </div>
  );
}