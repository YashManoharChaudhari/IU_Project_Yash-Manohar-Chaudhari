import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { motion } from "framer-motion";

export default function ResumeForm({ setResult, setError }) {
  const [jobDescription, setJobDescription] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    
    const filtered = acceptedFiles.filter(f =>
      (f.type === "application/pdf" || f.name.endsWith(".docx") || f.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    );
    setFiles(prev => {
      const next = [...prev];
      for (const f of filtered) {
        if (!next.some(n => n.name === f.name && n.size === f.size)) next.push(f);
      }
      return next;
    });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    multiple: true,
    maxFiles: 20
  });

  const removeFile = (name) => {
    setFiles(prev => prev.filter(f => f.name !== name));
  };

  const handleSubmit = async (e) => {
    e && e.preventDefault();
    setError("");
    setResult(null);

    if (!jobDescription.trim()) {
      setError("Please enter a job description");
      return;
    }
    if (files.length < 2) {
      setError("Please upload at least 2 resume files");
      return;
    }

    setLoading(true);
    try {
      const form = new FormData();
      form.append("job_description", jobDescription);
      files.forEach(f => form.append("files", f));

      const res = await axios.post("http://127.0.0.1:8002/api/select", form, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60_000
      });

      if (res.data?.status === "success") {
        setResult(res.data);
      } else {
        setError(res.data?.message || "Unexpected backend response");
      }
    } catch (err) {
      console.error(err);
      setError("Connection error — make sure the backend is running and CORS allows requests from this origin.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <form className="form-shell" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="label">Job Description</label>
          <textarea
            className="textarea"
            placeholder="Describe the role, required skills, years of experience..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={6}
          />
        </div>

        <div className="form-group">
          <label className="label">Upload Resumes</label>

          <div {...getRootProps()} className={`dropzone ${isDragActive ? "drag-active" : ""}`}>
            <input {...getInputProps()} />
            <div className="drop-inner">
              <strong>Drag & drop files here</strong>
              <span>or click to browse (PDF / DOCX)</span>
            </div>
          </div>

          <div className="file-list">
            {files.length === 0 && <small className="muted">No files selected yet</small>}
            {files.map((f) => (
              <div className="file-row" key={f.name + f.size}>
                <div className="file-meta">
                  <div className="file-icon">📄</div>
                  <div>
                    <div className="file-name">{f.name}</div>
                    <div className="file-size">{(f.size / 1024).toFixed(1)} KB</div>
                  </div>
                </div>
                <button type="button" className="btn-remove" onClick={() => removeFile(f.name)}>Remove</button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-actions">
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Analyzing…" : "Find Best Resume"}
          </button>
          <button
            type="button"
            className="btn-ghost"
            onClick={() => { setJobDescription(""); setFiles([]); setError(""); setResult(null); }}
          >
            Reset
          </button>
        </div>
      </form>
    </motion.div>
  );
}