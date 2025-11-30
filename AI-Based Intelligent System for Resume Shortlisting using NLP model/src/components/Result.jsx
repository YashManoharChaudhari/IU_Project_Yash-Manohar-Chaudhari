import React from "react";
import { motion } from "framer-motion";

export default function Result({ result }) {
  if (!result || !result.ranked_resumes) return null;

  return (
    <motion.div initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.45 }} className="result-block">
      <div className="result-header">
        <h3>📊 Resume Rankings</h3>
        <div className="score-pill">{result.total_resumes} resumes</div>
      </div>

      <div className="result-body">
        {result.ranked_resumes.map((resume, index) => (
          <div key={resume.name} className="resume-card">
            <div className="resume-title">
              <span className="rank-badge">#{resume.rank || index + 1}</span>
              {resume.name}
            </div>
            <div className="meta-row">
              <div>Match Score: {(resume.similarity_score * 100).toFixed(1)}%</div>
              <div>Raw Score: {resume.similarity_score.toFixed(3)}</div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}