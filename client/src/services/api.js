/**
 * Base API configuration and generic request handler
 */
const getApiUrl = () => {
  return (typeof window !== 'undefined' && window.__API_URL__) 
    || process.env.VUE_APP_API_URL 
    || 'http://localhost:8000';
};

export const apiClient = {
  baseUrl: getApiUrl(),
  
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });
      
      if (!response.ok) {
        throw new ApiError(`HTTP error! status: ${response.status}`, response.status);
      }
      
      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError(error.message, 0, error);
    }
  },
  
  get(endpoint, params) {
    const queryString = params ? `?${new URLSearchParams(params)}` : '';
    return this.request(`${endpoint}${queryString}`);
  },
};

export class ApiError extends Error {
  constructor(message, status, originalError = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.originalError = originalError;
  }
  
  get isNetworkError() {
    return this.status === 0;
  }
  
  get isServerError() {
    return this.status >= 500;
  }
}
