import { authStore } from '../store/auth';

export default function LogoutButton() {
  const logout = () => { authStore.clear(); window.location.href = '/login'; };
  return <button onClick={logout}>Logout</button>;
}
