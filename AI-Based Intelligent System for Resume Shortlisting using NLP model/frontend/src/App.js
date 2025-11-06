import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }
    
    if (files.length < 2) {
      setError('Please select at least 2 resume files');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/select', formData);
      
      if (response.data.status === 'success') {
        setResult(response.data);
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('Connection error. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div className="header">
          <h1>Resume Selector</h1>
          <p>Find the best matching resume using keyword analysis</p>
        </div>
        
        <div className="content">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Job Description</label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Enter job description here..."
                required
              />
            </div>
            
            <div className="form-group">
              <label>Upload Resume Files</label>
              <input
                type="file"
                multiple
                accept=".pdf,.docx"
                onChange={(e) => setFiles(e.target.files)}
                required
              />
              <small>Select 2 or more resume files (PDF or DOCX)</small>
            </div>
            
            <button type="submit" disabled={loading}>
              {loading ? 'Analyzing...' : 'Find Best Resume'}
            </button>
          </form>
          
          {error && (
            <div className="error">
              <strong>Error:</strong> {error}
            </div>
          )}
          
          {result && (
            <div className="success">
              <h3>Ranked Results ({result.total_resumes} candidates)</h3>
              {result.ranked_resumes.map((resume, index) => (
                <div key={index} className={`resume-item ${index === 0 ? 'top-match' : ''}`}>
                  <div className="rank">#{index + 1}</div>
                  <div className="resume-info">
                    <div className="resume-name">{resume.name}</div>
                    <div className="score">
                      {(resume.similarity_score * 100).toFixed(1)}% match
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;