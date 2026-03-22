import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
    const body = { prompt };
    if (systemInstruction) body.system_instruction = systemInstruction;
    
    const response = await api.post('/api/test-vulnerable', body);
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

// Submit prompt through two-stage pipeline (detection + conditional LLM call)
export const submitPrompt = async (prompt, systemInstruction = null) => {
  try {
    const body = { prompt };
    if (systemInstruction) body.system_instruction = systemInstruction;
    
    const response = await api.post('/api/analyze', body);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to submit prompt');
  }
};

// Test improved prompt
export const testImprovedPrompt = async (prompt, systemInstruction = null) => {
  try {
    const body = { prompt };
    if (systemInstruction) body.system_instruction = systemInstruction;
    
    const response = await api.post('/api/test-improved-prompt', body);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to test improved prompt');
  }
};

export default api;
