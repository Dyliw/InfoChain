import apiConfig from "./config";

export const brokenPhoneAPI = {
  // Iniciar cadena
  start: (data) => apiConfig.post('/broken-phone/start', data),
  
  // Transmitir mensaje
  transmit: (data) => apiConfig.post('/broken-phone/transmit', data),
  
  // Obtener cadena completa
  getChain: (chainId) => apiConfig.get(`/broken-phone/chain/${chainId}`),
};
