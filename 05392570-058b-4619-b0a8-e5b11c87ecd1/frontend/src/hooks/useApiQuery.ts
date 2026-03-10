import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';

const useApiRequest = () => {
  const { token } = useAuth();

  const api = axios.create({
    baseURL: '/api',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  });

  return api;
};

export const useApiQuery = (key: string | any[], url: string, options = {}) => {
  const api = useApiRequest();
  return useQuery(key, () => api.get(url).then(res => res.data), options);
};

export const useApiMutation = (url: string, method: 'post' | 'put' | 'patch' | 'delete' = 'post') => {
  const api = useApiRequest();
  const queryClient = useQueryClient();

  return useMutation(
    (data?: any) => api[method](url, data).then(res => res.data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('captives');
      }
    }
  );
};
