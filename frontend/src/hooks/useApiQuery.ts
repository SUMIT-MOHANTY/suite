import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export function useApiQuery<T>(key: string[], path: string, options = {}) {
  return useQuery({
    queryKey: key,
    queryFn: async () => {
      const { data } = await axios.get(`/api${path}`, {
        withCredentials: true
      });
      return data as T;
    },
    ...options
  });
}
