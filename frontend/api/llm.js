import apiConfig from "./config";

export const llmAPI = {
  // Chat con IA
  chat: (data) => apiConfig.post('/llm/chat', data),
  
  // Auditar respuesta
  audit: (data) => apiConfig.post('/llm/audit', data),
  
  // Feedback de IA
  feedback: (data) => apiConfig.post('/llm/feedback', data),
  
  // Obtener interacciones
  getInteractions: (params = {}) => {
    const { skip = 0, limit = 50 } = params;
    return apiConfig.get('/llm/interactions', { params: { skip, limit } });
  },
  
  // Obtener interacción específica
  getInteraction: (interactionId) => 
    apiConfig.get(`/llm/interactions/${interactionId}`),
};
