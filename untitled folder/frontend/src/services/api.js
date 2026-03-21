import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analyze prompt for injection
export const analyzePrompt = async (prompt) => {
  try {
    const response = await api.post('/api/analyze', { prompt });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to analyze prompt');
  }
};

// Test prompt vulnerability with Gemini
export const testPromptVulnerability = async (prompt, systemInstruction = null) => {
  try {
    const response = await api.post('/api/test-vulnerable', {
      prompt,
      system_instruction: systemInstruction,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to test vulnerability');
  }
};

// Get fix suggestions
export const getFixSuggestions = async (prompt) => {
  try {
    const response = await api.post('/api/fix-prompt', { prompt });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get fix suggestions');
  }
};

// Test improved prompt
export const testImprovedPrompt = async (prompt, systemInstruction = null) => {
  try {
    const response = await api.post('/api/test-improved-prompt', {
      prompt,
      system_instruction: systemInstruction,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to test improved prompt');
  }
};

export default api;
