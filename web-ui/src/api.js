import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const runCircuit = async (circuitData) => {
  const response = await api.post('/run-circuit', circuitData);
  return response.data;
};

export const getAvailableGates = async () => {
  const response = await api.get('/gates');
  return response.data;
};

export const optimizeCircuit = async (circuitData) => {
  const response = await api.post('/optimize', circuitData);
  return response.data;
};

export const getBlochSphereData = async (circuitData) => {
  const response = await api.post('/bloch-sphere', circuitData);
  return response.data;
};

export default api;
