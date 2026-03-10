import axios from 'axios';
const api = axios.create({ baseURL: 'http://localhost:4000' });

export const apiService = {
  getTodos: () => api.get('/todos').then(r => r.data),
  createTodo: (title: string) => api.post('/todos', { title }).then(r => r.data),
  updateTodo: (id: string, data: any) => api.patch(`/todos/${id}`, data).then(r => r.data),
};

export const api = apiService;
