import React, { useState } from 'react';
import { getFixSuggestions, testPromptVulnerability } from '../services/api';
import '../styles/FixSuggestions.css';

function FixSuggestions({ prompt, onBack, onReset }) {
  const [loading, setLoading] = useState(true);
  const [fixes, setFixes] = useState(null);
  const [testingImproved, setTestingImproved] = useState(false);
  const [improvedResult, setImprovedResult] = useState(null);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    loadFixes();
  }, [prompt]);

  const loadFixes = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await getFixSuggestions(prompt);
      setFixes(result);
    } catch (err) {
      setError(err.message || 'Error getting fix suggestions');
    } finally {
      setLoading(false);
    }
  };

  const handleTestImprovedPrompt = async () => {
    if (!fixes || !fixes.improved_prompt) return;

    setTestingImproved(true);
    setError(null);

    try {
      const result = await testPromptVulnerability(fixes.improved_prompt);
      setImprovedResult(result);
    } catch (err) {
      setError(err.message || 'Error testing improved prompt');
    } finally {
      setTestingImproved(false);
    }
  };

  if (loading) {
    return (
      <div className="fix-suggestions">
        <div className="loading">Loading fix suggestions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fix-suggestions">
        <div className="error-message">{error}</div>
        <button className="btn-secondary" onClick={onBack}>← Back</button>
      </div>
    );
  }

  return (
    <div className="fix-suggestions">
      <div className="fixes-header">
        <h2>🔧 Fix Suggestions</h2>
        <p>Here's how to make your prompt more resistant to injection attacks</p>
      </div>

      {fixes && (
        <>
          <div className="fixes-container">
            <div className="fixes-explanation">
              <h3>Analysis</h3>
              <p>{fixes.explanation}</p>
            </div>

            <div className="fixes-list">
              <h3>Recommended Fixes:</h3>
              <ul>
                {fixes.fixes && fixes.fixes.length > 0 ? (
                  fixes.fixes.map((fix, idx) => (
                    <li key={idx}>
                      <strong>Fix {idx + 1}:</strong> {fix}
                    </li>
                  ))
                ) : (
                  <li>See explanation above for detailed fixes</li>
                )}
              </ul>
            </div>

            {fixes.improved_prompt && (
              <div className="improved-prompt">
                <h3>Improved Prompt:</h3>
                <div className="prompt-box original">
                  <p><strong>Original:</strong></p>
                  <p>{prompt}</p>
                </div>
                <div className="prompt-box improved">
                  <p><strong>Improved:</strong></p>
                  <p>{fixes.improved_prompt}</p>
                </div>

                <button 
                  className="btn-primary"
                  onClick={handleTestImprovedPrompt}
                  disabled={testingImproved}
                >
                  {testingImproved ? 'Testing...' : '✅ Test Improved Prompt'}
                </button>
              </div>
            )}

            {improvedResult && (
              <div className={`improvement-result ${!improvedResult.vulnerability_detected ? 'success' : 'warning'}`}>
                <h3>{!improvedResult.vulnerability_detected ? '✅ Improvement Validated!' : '⚠️ Still Vulnerable'}</h3>
                <p>The improved prompt is {!improvedResult.vulnerability_detected ? 'much more secure' : 'still vulnerable to attacks'}.</p>
                <p><strong>Result:</strong> {improvedResult.analysis}</p>
              </div>
            )}
          </div>

          <div className="completion-actions">
            <button className="btn-primary" onClick={onReset}>
              ← Analyze Another Prompt
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default FixSuggestions;
