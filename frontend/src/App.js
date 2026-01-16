import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [rawText, setRawText] = useState("");
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setRawText("");
  };

  const handleTextChange = (e) => {
    setRawText(e.target.value);
    setFile(null);
  };

  const handleSubmit = async () => {
    if (!file && !rawText) {
      setError("Please upload a file or paste raw text.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      let res;
      const formData = new FormData();
      if (file) {
        formData.append("file", file);
      } else {
        formData.append("raw_text", rawText);
      }
      res = await axios.post("http://127.0.0.1:8000/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResumeData(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze resume.");
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>AI Resume Analyzer</h1>

      <div className="input-section">
        <label className="label">Upload Resume (PDF)</label>
        <input type="file" onChange={handleFileChange} className="file-input" />

        <label className="label">Or Paste Raw Text</label>
        <textarea
          value={rawText}
          onChange={handleTextChange}
          placeholder="Paste resume text here..."
          className="text-input"
        ></textarea>

        <button onClick={handleSubmit} className="analyze-button">
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {error && <p className="error-text">{error}</p>}
      </div>

      {resumeData && (
        <div className="results">
          <h2>Results:</h2>
          <p><strong>Name:</strong> {resumeData.name}</p>
          <p><strong>Email:</strong> {resumeData.email}</p>
          <p><strong>Phone:</strong> {resumeData.phone}</p>
          <p><strong>Skills:</strong> {resumeData.skills.join(", ")}</p>
          <p><strong>Experience:</strong> {resumeData.experience_years} years ({resumeData.experience_level})</p>
          <p><strong>Classification:</strong> {resumeData.classification} ({resumeData.confidence})</p>

          <div>
            <strong>Education:</strong>
            {resumeData.education && resumeData.education.length > 0 ? (
              <ul>
                {resumeData.education.map((edu, idx) => (
                  <li key={idx}>
                    {edu.institution}{edu.degree ? `, ${edu.degree}` : ""}{edu.year ? ` (${edu.year})` : ""}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No education info found</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
