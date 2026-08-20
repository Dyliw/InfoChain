import apiConfig from "./config";

export const scenariosAPI = {
  // Obtener todos los escenarios
  getAll: (params = {}) => {
    const { skip = 0, limit = 100 } = params;
    return apiConfig.get('/scenarios', { params: { skip, limit } });
  },
  
  // Obtener un escenario por slug
  getBySlug: (slug) => apiConfig.get(`/scenarios/${slug}`),
  
  // Iniciar escenario
  start: (slug, data) => apiConfig.post(`/scenarios/${slug}/start`, data),
  
  // Procesar paso
  step: (slug, data) => apiConfig.post(`/scenarios/${slug}/step`, data),
  
  // Completar escenario
  complete: (slug, data) => apiConfig.post(`/scenarios/${slug}/complete`, data),
  
  // Obtener instancia
  getInstance: (instanceId) => apiConfig.get(`/scenarios/instance/${instanceId}`),
};
