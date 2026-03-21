import React from 'react';
import '../styles/AnalysisResult.css';

function AnalysisResult({ analysis, prompt, onTestVulnerability, onGetFixes, onReset }) {
  const riskLevel = analysis.risk_score > 70 ? 'High' : analysis.risk_score > 30 ? 'Medium' : 'Low';
  const riskColor = riskLevel === 'High' ? '#e74c3c' : riskLevel === 'Medium' ? '#f39c12' : '#27ae60';

  return (
    <div className="analysis-result">
      <div className="result-header">
        <h2>Analysis Results</h2>
        <button className="minimize-btn" onClick={() => window.scrollTo(0, 0)}>↑</button>
      </div>

      <div className="result-card">
        <div className="prompt-display">
          <h3>Your Prompt:</h3>
          <p className="prompt-text">"{prompt}"</p>
        </div>

        <div className="risk-indicator">
          <div className="risk-gauge">
            <div className="risk-bar" style={{ width: `${analysis.risk_score}%`, backgroundColor: riskColor }}></div>
          </div>
          <p>Risk Level: <strong style={{ color: riskColor }}>{riskLevel}</strong></p>
          <p>Risk Score: {analysis.risk_score.toFixed(1)}/100</p>
        </div>

        <div className="analysis-details">
          <div className={`status ${analysis.is_injection ? 'vulnerable' : 'safe'}`}>
            <h3>{analysis.is_injection ? '⚠️ Vulnerable' : '✅ Safe'}</h3>
            <p>{analysis.explanation}</p>
            <p>Confidence: {(analysis.confidence * 100).toFixed(1)}%</p>
          </div>
        </div>

        <div className="action-buttons">
          {analysis.is_injection && (
            <>
              <button className="btn-primary" onClick={onTestVulnerability}>
                🧪 Test Vulnerability with Gemini
              </button>
              <button className="btn-secondary" onClick={onGetFixes}>
                🔧 Get Fix Suggestions
              </button>
            </>
          )}
          <button className="btn-secondary" onClick={onReset}>
            ← Analyze Another Prompt
          </button>
        </div>
      </div>
    </div>
  );
}

export default AnalysisResult;
