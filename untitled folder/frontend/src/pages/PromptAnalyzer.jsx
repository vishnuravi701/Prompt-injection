import React, { useState } from 'react';
import PromptInput from '../components/PromptInput';
import AnalysisResult from '../components/AnalysisResult';
import VulnerabilityTest from '../components/VulnerabilityTest';
import FixSuggestions from '../components/FixSuggestions';
import { analyzePrompt } from '../services/api';
import '../styles/PromptAnalyzer.css';

function PromptAnalyzer() {
  const [prompt, setPrompt] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(0); // 0: Input, 1: Analysis, 2: Vulnerability Test, 3: Fix Suggestions

  const handleAnalyze = async (inputPrompt) => {
    setPrompt(inputPrompt);
    setLoading(true);
    setError(null);
    setStep(1);

    try {
      const result = await analyzePrompt(inputPrompt);
      setAnalysis(result);
    } catch (err) {
      setError(err.message || 'Error analyzing prompt');
      setStep(0);
    } finally {
      setLoading(false);
    }
  };

  const handleTestVulnerability = () => {
    setStep(2);
  };

  const handleGetFixes = () => {
    setStep(3);
  };

  const handleReset = () => {
    setPrompt('');
    setAnalysis(null);
    setError(null);
    setStep(0);
  };

  return (
    <div className="prompt-analyzer">
      {step === 0 && (
        <PromptInput onAnalyze={handleAnalyze} loading={loading} />
      )}
      
      {error && <div className="error-message">{error}</div>}
      
      {analysis && step >= 1 && (
        <AnalysisResult 
          analysis={analysis}
          prompt={prompt}
          onTestVulnerability={handleTestVulnerability}
          onGetFixes={handleGetFixes}
          onReset={handleReset}
        />
      )}
      
      {analysis && step === 2 && analysis.is_injection && (
        <VulnerabilityTest 
          prompt={prompt}
          onNext={handleGetFixes}
          onBack={() => setStep(1)}
        />
      )}
      
      {analysis && step === 3 && (
        <FixSuggestions 
          prompt={prompt}
          onBack={() => setStep(1)}
          onReset={handleReset}
        />
      )}
    </div>
  );
}

export default PromptAnalyzer;
