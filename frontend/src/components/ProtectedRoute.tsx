import { ReactNode } from 'react';
import { authStore } from '../store/auth';

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  if (!authStore.token) {
    window.location.href = '/login';
    return null;
  }
  return <>{children}</>;
}
