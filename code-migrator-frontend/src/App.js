import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [sourceCode, setSourceCode] = useState("");
  const [sourceLang, setSourceLang] = useState("python");
  const [targetLang, setTargetLang] = useState("java");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleMigrate = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/migrate", {
        source_code: sourceCode,
        source_language: sourceLang,
        target_language: targetLang,
      });

      setResult(response.data.migrated_code);
    } catch (error) {
      setResult("Error processing the request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Code Migrator</h1>

      <div>
        <label>Source Language:</label>
        <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
        </select>

        <label>Target Language:</label>
        <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
        </select>
      </div>

      <textarea
        rows="10"
        cols="80"
        placeholder="Enter your source code here..."
        value={sourceCode}
        onChange={(e) => setSourceCode(e.target.value)}
      />

      <button onClick={handleMigrate} disabled={loading}>
        {loading ? "Translating..." : "Migrate Code"}
      </button>

      <h2>Migrated Code</h2>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
