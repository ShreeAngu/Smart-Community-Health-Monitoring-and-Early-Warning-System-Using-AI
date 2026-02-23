import axios from 'axios';

const API_BASE_URL = 'http://localhost:000';

// Create axios instance
const api = axios.create({
 baseURL: API_BASE_URL,
 headers: {
 'Content-Type': 'application/json',
 },
});

// Add token to requests
api.interceptors.request.use((config) => {
 const token = localStorage.getItem('token');
 if (token) {
 config.headers.Authorization = `Bearer ${token}`;
 }
 return config;
});

// Handle token expiration
api.interceptors.response.use(
 (response) => response,
 (error) => {
 if (error.response?.status === 0) {
 localStorage.removeItem('token');
 localStorage.removeItem('user');
 window.location.href = '/login';
 }
 return Promise.reject(error);
 }
);

// Auth API
export const authAPI = {
 login: (email: string, password: string) =>
 api.post('/login', { email, password }),

 register: (email: string, password: string, role: 'community' | 'admin' = 'community') =>
 api.post('/register', { email, password, role }),

 getCurrentUser: () =>
 api.get('/auth/me'),
};

// Reports API
export const reportsAPI = {
 submitReport: (reportData: any) =>
 api.post('/submit-report', reportData),

 getReports: (skip = 0, limit = 00) =>
 api.get(`/reports?skip=${skip}&limit=${limit}`),

 getWeeklySummary: () =>
 api.get('/reports/weekly'),

 exportReports: (days = ) =>
 api.get(`/reports/export?days=${days}`, { responseType: 'blob' }),
};

// Predictions API
export const predictionsAPI = {
 predictRisk: (reportData: any) =>
 api.post('/predict-risk', reportData),

 getPredictions: (skip = 0, limit = 00) =>
 api.get(`/predictions?skip=${skip}&limit=${limit}`),

 getRegionalRisk: () =>
 api.get('/regional-risk'),

 getFeatureImportance: () =>
 api.get('/feature-importance'),

 getRegionalDrivers: (region: string, days = ) =>
 api.get(`/regional-risk/${encodeURIComponent(region)}/drivers`, { params: { days } }),
};

// Alerts API
export const alertsAPI = {
 getAlerts: (skip = 0, limit = 00) =>
 api.get(`/alerts?skip=${skip}&limit=${limit}`),

 createAlert: (alertData: any) =>
 api.post('/alerts', alertData),

 updateAlertStatus: (alertId: number, status: 'active' | 'resolved' | 'dismissed', resolvedBy?: number) =>
 api.patch(`/alerts/${alertId}`, { status, resolved_by: resolvedBy }),

 dismissAlert: (alertId: number, userId?: number) =>
 api.patch(`/alerts/${alertId}`, { status: 'dismissed', resolved_by: userId }),

 resolveAlert: (alertId: number, userId?: number) =>
 api.patch(`/alerts/${alertId}`, { status: 'resolved', resolved_by: userId }),
};

// Dashboard API
export const dashboardAPI = {
 getStats: () =>
 api.get('/dashboard'),
};

export default api;