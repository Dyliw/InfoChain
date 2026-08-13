  import apiConfig from "./config";


export const analysisAPI = {
  decompose: (data) => apiConfig.post('/analysis/decompose', data),
  compare: (data) => apiConfig.post('/analysis/compare', data),
  save: (data) => apiConfig.post('/analysis/save', data),
  getById: (analysisId) => apiConfig.get(`/analysis/${analysisId}`),
};
