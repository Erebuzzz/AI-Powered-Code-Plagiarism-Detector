import axios from 'axios';

// Single consistent API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Upload files for comparison
  uploadFiles: async (file1, file2, language1, language2) => {
    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);
    formData.append('language1', language1);
    formData.append('language2', language2);

    const response = await api.post('/api/comparison/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Compare code snippets
  compareCode: async (code1, code2, language1, language2) => {
    try {
      const response = await api.post('/api/comparison/compare', {
        code1,
        code2,
        language1,
        language2
      });
      return response.data;
    } catch (error) {
      console.error('Error comparing code:', error);
      throw error;
    }
  },

  // Get comparison report
  getReport: async (comparisonId) => {
    const response = await api.get(`/api/comparison/report/${comparisonId}`);
    return response.data;
  },

  // Get comparison history
  getHistory: async (limit = 10) => {
    const response = await api.get(`/api/comparison/history?limit=${limit}`);
    return response.data;
  },
  
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error', message: error.message };
    }
  }
};

export default apiService;