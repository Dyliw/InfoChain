import apiConfig from "./config";

export const mapsAPI = {
  // Generar mapa de razonamiento
  generate: (data) => apiConfig.post('/maps/generate', data),
  
  // Obtener mapa por analysis_id
  getByAnalysisId: (analysisId) => apiConfig.get(`/maps/${analysisId}`),
  
  // Guardar mapa con ajustes
  save: (data) => apiConfig.post('/maps/save', data),
};
