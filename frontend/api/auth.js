import apiConfig from "./config";


export const authAPI = {
  register: (data) => apiConfig.post('/auth/register', data),
  
  login: (data) => apiConfig.post('/auth/login', data),
  
  refresh: (refreshToken) => apiConfig.post('/auth/refresh', { refresh_token: refreshToken }),
  
  getMe: () => apiConfig.get('/auth/me'),
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  
  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  },
};
